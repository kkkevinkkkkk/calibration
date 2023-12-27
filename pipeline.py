from transformers import pipeline, TextGenerationPipeline, AutoModelForTokenClassification, AutoTokenizer
import torch.nn.functional as F
from transformers.pipelines.text_generation import ReturnType
import torch
import transformers
import openai
import os
import re
from retry import retry
from openai.error import Timeout, APIError, ServiceUnavailableError
from omegaconf import DictConfig
from nltk.corpus import stopwords
from nltk import sent_tokenize
from string import punctuation
import numpy as np

from utils import NERModel
from collections import defaultdict

from prompter import Prompter

from omegaconf import OmegaConf

OPENAI_MODELS = ["gpt-4", "gpt-3.5-turbo", "gpt-4-1106-preview"]
openai.api_key = os.getenv("OPENAI_API_KEY")


def pipeline_init(**kwargs):
    if kwargs["model"] in OPENAI_MODELS:
        if kwargs["model"] == "gpt-4":
            kwargs["model"] = "gpt-4-1106-preview"
            print("use gpt-4-turbo")
        return kwargs["pipeline_class"](**kwargs)
    else:
        return transformers.pipeline(**kwargs)


def Record(generated_text=None,
           seq_log_prob=0,
           full_text="",
           **kwargs):
    d = {
        "generated_text": generated_text,
        "seq_log_prob": seq_log_prob,
        "full_text": full_text
    }
    d.update(kwargs)
    return d


class MyPipeline(TextGenerationPipeline):
    def __init__(self, *args, **kwargs):
        self.model_name = kwargs["model_name"] if "model_name" in kwargs else kwargs["model"]
        self.openai = True if self.model_name in OPENAI_MODELS else False

        def is_trained_model(s):
            pattern = r'^\d+\.\d+\.\d+$'
            return bool(re.match(pattern, s))

        if "vicuna" in self.model_name:
            self.model_type = "vicuna"
        elif "chat" in self.model_name or is_trained_model(self.model_name):
            self.model_type = "chat"
        else:
            self.model_type = "openai"

        if not self.openai:
            super().__init__(*args, **kwargs)
            self._forward_params = {}

    def _forward(self, model_inputs, **generate_kwargs):
        input_ids = model_inputs["input_ids"]
        attention_mask = model_inputs.get("attention_mask", None)
        # Allow empty prompts
        if input_ids.shape[1] == 0:
            input_ids = None
            attention_mask = None
            in_b = 1
        else:
            in_b = input_ids.shape[0]
        prompt_text = model_inputs.pop("prompt_text")

        # If there is a prefix, we may need to adjust the generation length. Do so without permanently modifying
        # generate_kwargs, as some of the parameterization may come from the initialization of the pipeline.
        prefix_length = generate_kwargs.pop("prefix_length", 0)
        if prefix_length > 0:
            has_max_new_tokens = "max_new_tokens" in generate_kwargs or (
                    "generation_config" in generate_kwargs
                    and generate_kwargs["generation_config"].max_new_tokens is not None
            )
            if not has_max_new_tokens:
                generate_kwargs["max_length"] = generate_kwargs.get("max_length") or self.model.config.max_length
                generate_kwargs["max_length"] += prefix_length
            has_min_new_tokens = "min_new_tokens" in generate_kwargs or (
                    "generation_config" in generate_kwargs
                    and generate_kwargs["generation_config"].min_new_tokens is not None
            )
            if not has_min_new_tokens and "min_length" in generate_kwargs:
                generate_kwargs["min_length"] += prefix_length
        generate_kwargs["output_scores"] = True
        generate_kwargs["return_dict_in_generate"] = True
        # generation_config = GenerationConfig(**generate_kwargs)
        # BS x SL
        # generated_sequence = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, generation_config=generation_config)
        generated_sequence = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, **generate_kwargs)
        scores = generated_sequence["scores"]
        generated_sequence = generated_sequence["sequences"]
        seq_tokens = generated_sequence[:, -len(scores):]
        scores_tokens = [(F.log_softmax(scores[t], dim=-1), seq_tokens[:, t]) for t in range(len(scores))]
        sampled_scores = [
            scores_t.gather(-1, token_t.unsqueeze(-1))
            for scores_t, token_t in scores_tokens
        ]
        sampled_scores = torch.cat(sampled_scores, dim=1)

        out_b = generated_sequence.shape[0]
        if self.framework == "pt":
            generated_sequence = generated_sequence.reshape(in_b, out_b // in_b, *generated_sequence.shape[1:])
        return {"generated_sequence": generated_sequence, "input_ids": input_ids,
                "prompt_text": prompt_text, "scores": sampled_scores}

    @staticmethod
    def post_process_cal_logprob(tokens_probs):
        filtered_cnt = 0
        filtered_logprob_sum = 0
        logprob_sum = 0
        cnt = 0
        for (token, prob) in tokens_probs:
            if token not in stopwords.words("english") and token != "<unk>" and token not in punctuation:
                filtered_logprob_sum += np.log(prob)
                filtered_cnt += 1
            if token != "<unk>":
                logprob_sum += np.log(prob)
                cnt += 1
        filtered_logprob = filtered_logprob_sum / filtered_cnt if filtered_cnt > 0 else 0
        logprob = logprob_sum / cnt if cnt > 0 else 0
        return {"seq_log_prob_average": logprob, "seq_log_prob_filtered": filtered_logprob}

    def postprocess(self, model_outputs, return_type=ReturnType.NEW_TEXT, clean_up_tokenization_spaces=True):
        generated_sequence = model_outputs["generated_sequence"][0]
        input_ids = model_outputs["input_ids"]
        prompt_text = model_outputs["prompt_text"]
        scores = model_outputs["scores"]
        tokens_probs_list = [[(self.tokenizer.decode(token), torch.exp(score).item())
                              for score, token in zip(scores[i], generated_sequence[i][-len(scores[i]):])] for i in
                             range(len(scores))]

        scores_copy = scores.clone()
        scores_copy[scores_copy == -float('inf')] = 0
        seq_log_probs = torch.sum(scores_copy, dim=-1)

        generated_sequence = generated_sequence.numpy().tolist()
        records = []
        for i, sequence in enumerate(generated_sequence):
            if return_type == ReturnType.TENSORS:
                record = {"generated_token_ids": sequence}
            elif return_type in {ReturnType.NEW_TEXT, ReturnType.FULL_TEXT}:
                # Decode text
                text = self.tokenizer.decode(
                    sequence,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                )

                # Remove PADDING prompt of the sequence if XLNet or Transfo-XL model is used
                if input_ids is None:
                    prompt_length = 0
                else:
                    prompt_length = len(
                        self.tokenizer.decode(
                            input_ids[0],
                            skip_special_tokens=True,
                            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                        )
                    )

                all_text = text[prompt_length:]
                full_text = prompt_text + all_text
                if return_type == ReturnType.FULL_TEXT:
                    all_text = prompt_text + all_text

                # record = {"generated_text": all_text, "tokens_probs": tokens_probs_list[i],
                #           "seq_log_prob": seq_log_probs[i].item(), "full_text": full_text}
                record = {"generated_text": all_text, "seq_log_prob": seq_log_probs[i].item(), "full_text": full_text,
                          "output": all_text}
                log_probs = self.post_process_cal_logprob(tokens_probs_list[i])
                record.update(log_probs)
                record = Record(**record)
            records.append(record)

        return records

    @retry((Timeout, APIError, ServiceUnavailableError), tries=50, delay=1, backoff=6, max_delay=300)
    def get_openai_completion(self, prompt, temperature=1.0, model_name=None):
        messages = [{"role": "user", "content": prompt}]
        model_name = model_name if model_name is not None else self.model_name

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=temperature, )
        output = response.choices[0].message["content"]

        record = Record(**{"generated_text": output,
                           "seq_log_prob": 0, "full_text": prompt + "\n" + output,
                           "output": output})
        records = [record]
        return records

    @staticmethod
    def get_openai_completion_static(prompt, temperature=1.0, model_name=None):
        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=temperature, )
        output = response.choices[0].message["content"]

        record = Record(**{"generated_text": output,
                           "seq_log_prob": 0, "full_text": prompt + "\n" + output,
                           "output": output})
        records = [record]
        return records

    @staticmethod
    def extract_score(text, pattern=r"(\d+)/100"):
        match = re.search(pattern, text)
        if not match:
            print("Warning!!!", text)
        score = int(match.group(1)) if match else 0
        return score

    def __call__(self, inputs, *args, temperature=0.6,
                 num_workers=None, batch_size=None, random_state=1, **kwargs):

        if self.openai:
            return self.get_openai_completion(inputs, temperature=temperature)
        else:
            kwargs["temperature"] = temperature
            torch.cuda.manual_seed(random_state)
            records = super().__call__(inputs, **kwargs)
            return records

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0, **kwargs):
        output = {}
        return output

    @staticmethod
    def extract_confidence_distribution(scores, category_num=6):
        confidence_distribution = [0] * category_num
        score_interval = 100 / (category_num - 1)
        for score in scores:
            if np.isnan(score):
                score = 0
            confidence_distribution[int(round(score / score_interval))] += 1 / len(scores)
        confidence_distribution = [round(confidence_distribution[i], 3) for i in range(category_num)]
        return confidence_distribution


class SelfEvalPipeline(MyPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def extract_confidence_score(self, answer, question,
                                 dataset_name="asqa",
                                 temperature=0.6,
                                 five_pnt=True, **kwargs):
        if five_pnt:
            inputs = Prompter(model_name=self.model_name, dataset_name=dataset_name).generate_text_input(
                question=question, answer=answer, task_type="self_eval")
        else:
            raise NotImplementedError
        outputs = self.__call__(inputs, num_return_sequences=1, temperature=temperature)

        output = {"inputs_self_eval": inputs}
        comment = outputs[0]["generated_text"]

        if five_pnt:
            correctness_score = self.extract_score(comment, pattern=r"Score: (\d+)/5") * 20
        else:
            correctness_score = self.extract_score(comment, pattern=r"Correctness Score: (\d+)/100")

        output["comment_self_eval"] = comment
        output["score_self_eval"] = correctness_score
        return output


class SelfEvalRangePipeline(SelfEvalPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0.6, **kwargs):
        inputs = Prompter(model_name=self.model_name, dataset_name=dataset_name).generate_text_input(
            question=question, answer=answer, task_type="self_eval_range")
        outputs = self.__call__(inputs, temperature=temperature)
        comment = outputs[0]["generated_text"]
        pattern = r"(\d+)-(\d+)/5"
        match = re.search(pattern, comment)
        if not match:
            print("Warning!!! Not find score range in", comment)
        score_low = int(match.group(1)) if match else 0
        score_high = int(match.group(2)) if match else 0
        confidence_distribution = self.extract_confidence_distribution(score_low, score_high)

        output = {
            "inputs_self_eval_range": inputs,
            "comment_self_eval_range": comment,
            "correctness_score_high": score_high,
            "correctness_score_low": score_low,
            "confidence_distribution": confidence_distribution,
        }
        return output

    @staticmethod
    def extract_confidence_distribution(score_low, score_high, category_num=6):
        if score_low > score_high:
            print(f"warning low score is higher than high score, {score_low} > {score_high}")
            tmp = score_low
            score_low = score_high
            score_high = tmp
        confidence_distribution = [0] * category_num
        for score in range(score_low, score_high + 1):
            confidence_distribution[score] = 1 / (score_high - score_low + 1)
        return confidence_distribution



class EvaluationPipeline(MyPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def evaluate_answer(self, answer, question, gold_answer, dataset_name="asqa",
                        use_examples=True, five_pnt=False, temperature=0,
                        **kwargs):
        inputs = Prompter(model_name=self.model_name, dataset_name=dataset_name).generate_text_input(
            question=question, answer=answer, reference_answer=gold_answer, task_type="eval")

        outputs = self.__call__(inputs, temperature=temperature, **kwargs)
        comment = outputs[0]["generated_text"]
        if five_pnt:
            score = self.extract_score(comment, pattern=r"Score: (\d+)/5") * 20
        else:
            score = self.extract_score(comment)


        fact_inputs = ""
        fact_comment = ""
        fact_score = 0

        output = {
            "inputs_eval": inputs,
            "comment": comment,
            "score": score,
            "fact_inputs_eval": fact_inputs,
            "fact_comment": fact_comment,
            "fact_score": fact_score
        }
        return output


class SelfRepetitionPipeline(MyPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, inputs, *args, temperature=0.6,
                 num_workers=None, batch_size=None, num_return_sequences=1, random_state=1, **kwargs):
        sequences = []
        for i in range(num_return_sequences):
            outputs = super().__call__(inputs, *args, temperature=temperature,
                                       num_workers=num_workers, batch_size=batch_size,
                                       num_return_sequences=1, random_state=random_state + i, **kwargs)
            sequences.append(outputs[0])
        return sequences


    def evaluate_repetition(self, answer1, answer2, question, **kwargs):
        inputs = Prompter(model_name="openai").generate_text_input(
            question=question, answer1=answer1, answer2=answer2, task_type="repetition")
        outputs = self.get_openai_completion(inputs, model_name="gpt-3.5-turbo")
        comment = outputs[0]["generated_text"]
        score = self.extract_score(comment, pattern=r"Similarity score: (\d+)/5") * 20
        # score = self.extract_score(comment)

        output = {
            "inputs": inputs,
            "comment": comment,
            "score": score,
        }
        return output

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0.6, other_answers=None,
                                 **kwargs):
        scores = []
        outputs = {}
        for i, answer_ in enumerate(other_answers):
            output = self.evaluate_repetition(answer, answer_, question)
            scores.append(output["score"])
            outputs["inputs_repetition" + str(i)] = output["inputs"]
            outputs["comment_repetition" + str(i)] = output["comment"]
            outputs["score_repetition" + str(i)] = output["score"]

        total_score = np.mean(scores)
        outputs["score_repetition"] = total_score
        outputs["scores_repetition"] = scores
        outputs["other_answers"] = other_answers
        outputs["confidence_distribution"] = self.extract_confidence_distribution(scores)
        return outputs


class SelfRepetitionSplitPipeline(SelfRepetitionPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def evaluate_repetition(self, answer1, answer2, question=None, **kwargs):
        sentences = sent_tokenize(answer1)
        sentences_hit = []
        prompter_ = Prompter(model_name="openai")
        for sentence in sentences:
            inputs = prompter_.generate_text_input(sentence=sentence, response=answer2, task_type="repetition_split")
            outputs = self.get_openai_completion(inputs, model_name="gpt-3.5-turbo")
            comment = outputs[0]["generated_text"]
            if "yes" in comment.lower():
                sentences_hit.append(1)
            else:
                sentences_hit.append(0)
        score = np.mean(sentences_hit) * 100

        output = {
            "score": score,
            "sentences_hit": sentences_hit,
            "sentences": sentences,
        }
        return output

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0.6, other_answers=None,
                                 **kwargs):
        scores = []
        outputs = {}
        sentences_hits = []
        for i, answer_ in enumerate(other_answers):
            output = self.evaluate_repetition(answer, answer_, question)
            scores.append(output["score"])
            outputs["score_repetition_split" + str(i)] = output["score"]
            sentences_hits.append(output["sentences_hit"])
            sentences = output["sentences"]

        total_score = np.mean(scores)
        outputs["score_repetition_split"] = total_score
        outputs["scores_repetition_split"] = scores
        outputs["other_answers"] = other_answers
        outputs["sentences_hits"] = sentences_hits
        outputs["sentences"] = sentences
        return outputs


class SelfRepetitionClaimPipeline(SelfRepetitionPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.claim_detector = pipeline("text-classification",
                                       model="lucafrost/ClaimBuster-DeBERTaV2",)


    def evaluate_repetition(self, answer1, answer2, question=None, **kwargs):
        sentences = sent_tokenize(answer1)
        sentences_hit = []
        claim_labels = []
        claim_cnt = 0
        prompter_ = Prompter(model_name="openai")

        for sentence in sentences:
            claim_label = self.claim_detector(sentence)[0]["label"]

            if "NFS" not in claim_label:
                claim_cnt += 1
                inputs = prompter_.generate_text_input(sentence=sentence, response=answer2, task_type="repetition_split")

                outputs = self.get_openai_completion(inputs, model_name="gpt-3.5-turbo")
                comment = outputs[0]["generated_text"]
                if "yes" in comment.lower():
                    sentences_hit.append(1)
                else:
                    sentences_hit.append(0)
            else:
                sentences_hit.append(0)
            claim_labels.append(claim_label)


        if claim_cnt == 0:
            print("Warning! No claims found in answer:", answer1, "sentences:", sentences, "claim_labels:", claim_labels)
            score = 100
        else:
            score = np.sum(sentences_hit) / claim_cnt * 100

        output = {
            "score": score,
            "sentences_hit": sentences_hit,
            "sentences": sentences,
            "claim_labels": claim_labels,
        }
        return output

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0.6, other_answers=None,
                                 **kwargs):
        scores = []
        outputs = {}
        sentences_hits = []
        assert len(other_answers) > 0
        for i, answer_ in enumerate(other_answers):
            output = self.evaluate_repetition(answer, answer_, question)
            scores.append(output["score"])
            # outputs["score_repetition_claim" + str(i)] = output["score"]
            sentences_hits.append(output["sentences_hit"])

            sentences = output["sentences"]
            claim_labels = output["claim_labels"]

        total_score = np.mean(scores)
        outputs["score_repetition_claim"] = total_score
        outputs["scores_repetition_claim"] = scores
        outputs["other_answers"] = other_answers
        outputs["sentences_hits"] = sentences_hits
        outputs["sentences"] = sentences
        outputs["claim_labels"] = claim_labels
        return outputs


class SelfRepetitionNERPipeline(SelfRepetitionPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ner_model = NERModel()

    def get_entity_groups(self, question, entity_num=3, **kwargs):
        inputs = Prompter(model_name=self.model_name).generate_text_input(
            question=question, task_type="choose_entities", entity_num=entity_num)
        outputs = self.__call__(inputs)
        chosen_entities_text = outputs[0]["generated_text"]
        entity_groups = self.ner_model.extract_chosen_entities(chosen_entities_text)
        if len(entity_groups) != entity_num:
            print("Warning!!! Didn't find enough entities in comment:", chosen_entities_text)
        return entity_groups

    def evaluate_repetition(self, answer1, answer2, question, entity_num=5, entity_groups=None, dataset_name="asqa", **kwargs):
        if entity_groups is None:
            # entity_groups = self.get_entity_groups(question, entity_num=entity_num)
            entity_groups = list(self.ner_model.entity_groups.keys()) + ["ALL"]

        split = 0
        if dataset_name == "qampari":
            split = 2 if "chat" in self.model_name else 1
        entities_dict1 = self.ner_model.get_entities_dict(answer1, split)
        entities_dict2 = self.ner_model.get_entities_dict(answer2, split)

        total_num_1 = 0
        total_num_2 = 0
        overlap_num = 0
        overlap_entities = []
        for entity_group in entity_groups:
            total_num_1 += len(entities_dict1[entity_group])
            total_num_2 += len(entities_dict2[entity_group])
            for entity in entities_dict1[entity_group]:
                if entity in entities_dict2[entity_group]:
                    overlap_num += 1
                    overlap_entities.append(entity)
        score_precision = 0
        score_recall = 0
        score_f1 = 0
        if total_num_1 == 0:
            print("Warning!!! Didn't find any entities in answer 1:", answer1, entities_dict1)
            score = 0
        elif total_num_2 == 0:
            print("Warning!!! Didn't find any entities in answer 2:", answer2, entities_dict2)
            score = 0
        else:
            print(f"total_num_1: {total_num_1}, total_num_2: {total_num_2}, overlap_num: {overlap_num}")
            score_precision = overlap_num / total_num_1 * 100
            score_recall = overlap_num / total_num_2 * 100
            if score_precision + score_recall > 0:
                score_f1 = 2 * score_precision * score_recall / (score_precision + score_recall)
            else:
                score_f1 = 0
            score = score_precision
        # print(total_num, overlap_num)

        # turn set into list
        entities_dict1 = {k: list(v) for k, v in entities_dict1.items()}
        entities_dict2 = {k: list(v) for k, v in entities_dict2.items()}
        output = {
            "score": score,
            "score_precision": score_precision,
            "score_recall": score_recall,
            "score_f1": score_f1,
            "overlap_entities": overlap_entities,
            "entity_groups": entity_groups,
            "entities_dict1": entities_dict1,
            "entities_dict2": entities_dict2,
        }
        return output

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0.6, other_answers=None,
                                 **kwargs):
        scores = []
        scores_precision = []
        scores_recall = []
        scores_f1 = []

        outputs = {}
        results_dict = defaultdict(list)
        for i, answer_ in enumerate(other_answers):
            output = self.evaluate_repetition(answer, answer_, question, dataset_name=dataset_name)
            scores.append(output["score"])
            scores_precision.append(output["score_precision"])
            scores_recall.append(output["score_recall"])
            scores_f1.append(output["score_f1"])

            results_dict['overlap_entities'].append(output["overlap_entities"])
            results_dict['entities_dicts1'].append(output["entities_dict1"])
            results_dict['entities_dicts2'].append(output["entities_dict2"])

        total_score = np.mean(scores)
        outputs["entity_groups"] = output["entity_groups"]
        outputs["score_repetition_ner"] = total_score
        outputs["scores_repetition_ner"] = scores

        outputs["scores_precision"] = scores_precision
        outputs["scores_recall"] = scores_recall
        outputs["scores_f1"] = scores_f1
        outputs["score_precision"] = np.mean(scores_precision)
        outputs["score_recall"] = np.mean(scores_recall)
        outputs["score_f1"] = np.mean(scores_f1)

        outputs["other_answers"] = other_answers

        outputs.update(results_dict)
        return outputs


class SelfEvalRepetitionPipeline(SelfRepetitionPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def extract_score(text, pattern=r"(\d+)/100"):
        match = re.search(pattern, text)
        if not match:
            print("Warning!!!", text)

        score = int(match.group(1)) if match else 0
        return score, match
    def extract_scores(self, text, five_pnt=False):
        if five_pnt:
            correctness_score, match = self.extract_score(text, pattern=r"Score: (\d+)/5")
            if not match:
                correctness_score, match = self.extract_score(text, pattern=r"(\d+)/5")
            correctness_score *= 20
        else:
            correctness_score, match = self.extract_score(text, pattern=r"Correctness Score: (\d+)/100")
        # confidence_score = self.extract_score(text, pattern=r"Confidence Score: (\d+)/100")
        confidence_score = 0
        return correctness_score, confidence_score

    def extract_confidence_score(self, answer, question,
                                 dataset_name="asqa",
                                 temperature=0.6,
                                 num_return_sequences=10,
                                 five_pnt=True, n_doc=0,
                                 oracle_doc=False,
                                 **kwargs):
        if five_pnt:
            if n_doc > 0 or oracle_doc:
                inputs = Prompter(model_name=self.model_name, dataset_name=dataset_name,
                                  n_doc=n_doc).generate_text_input(
                    question=question, answer=answer, task_type="self_eval_doc", eval_item=kwargs["eval_item"],
                    oracle_doc=oracle_doc)
            else:
                inputs = Prompter(model_name=self.model_name, dataset_name=dataset_name).generate_text_input(
                    question=question, answer=answer, task_type="self_eval")

        else:
            raise NotImplementedError
        # print(inputs)
        outputs = self.__call__(inputs, num_return_sequences=num_return_sequences, temperature=temperature)
        scores = []
        output = {"inputs_self_eval": inputs}
        for i in range(num_return_sequences):
            comment = outputs[i]["generated_text"]
            correctness_score, confidence_score = self.extract_scores(comment, five_pnt)
            scores.append(correctness_score)
            output["comment_self_eval_" + str(i)] = comment

        output["score_self_eval"] = np.mean(scores)
        output["score_self_eval_std"] = np.std(scores)
        output["scores_self_eval"] = scores
        output["confidence_distribution"] = self.extract_confidence_distribution(scores)
        return output

    @staticmethod
    def extract_confidence_distribution(scores, category_num=6):
        confidence_distribution = [0] * category_num
        score_interval = 100 / (category_num - 1)
        for score in scores:
            confidence_distribution[int(score // score_interval)] += 1 / len(scores)
        return confidence_distribution
class SelfVerificationPipeline(SelfRepetitionPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract_confidence_score(self, answer, question,
                                 dataset_name="asqa",
                                 temperature=0.6,
                                 num_return_sequences=10,
                                 **kwargs):
        inputs = None
        raise NotImplementedError

        outputs = self.__call__(inputs, num_return_sequences=num_return_sequences, temperature=temperature)
        scores = []
        comments = []
        output = {"inputs_self_verification": inputs}
        for i in range(num_return_sequences):
            comment = outputs[i]["generated_text"]
            scores.append(1 if "true" in comment.lower() else 0)
            comments.append(comment)

        output["score_self_verification"] = np.mean(scores) * 100
        return output

class RephraseConsistencyPipeline(MyPipeline):
    def __init__(self, *args, rephrase_num=10, **kwargs):
        self.rephrase_num = rephrase_num
        super().__init__(*args, **kwargs)

    @staticmethod
    def extract_questions(text, pattern=r'Question \d+: (.+?)\n'):
        text = text + "\n"
        matches = re.findall(pattern, text)
        questions = [match for match in matches]
        if len(questions) != 10:
            print(f"warning!!! There are only {len(questions)} generated rephrased questions for {text}")
        return questions

    def rephrase_question(self, question, temperature=0.6, **kwargs):
        inputs = Prompter(model_name=self.model_name).generate_text_input(
            question=question, task_type="question_rephrase", rephrase_num=self.rephrase_num)
        outputs = self.__call__(inputs, temperature=temperature, **kwargs)
        comment = outputs[0]["generated_text"]
        questions = self.extract_questions(comment)
        return questions

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0.6, **kwargs):
        questions = self.rephrase_question(question, temperature=temperature)
        scores = []
        for question_ in questions:
            inputs = Prompter(model_name="openai").generate_text_input(
                question=question, task_type="compare_questions", question1=question, question2=question_)
            outputs = self.get_openai_completion(inputs, model_name="gpt-3.5-turbo")
            comment = outputs[0]["generated_text"]
            if comment.lower().startswith("yes") or comment.lower().startswith(" yes"):
                scores.append(1)
            elif comment.lower().startswith("no") or comment.lower().startswith(" no"):
                scores.append(0)
            else:
                scores.append(0)
                print("warning!!! Didn't find yes or no in comment:", comment)

        total_score = np.mean(scores) * 100
        return {"score_rephrase_consistency": total_score,
                "rephrased_questions": questions,
                "scores_rephrase_consistency": scores}


