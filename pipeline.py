from transformers import Pipeline, pipeline, TextGenerationPipeline
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
from string import punctuation
import numpy as np
from omegaconf import OmegaConf
OPENAI_MODELS =["gpt-4", "gpt-3.5-turbo"]
openai.api_key = os.getenv("OPENAI_API_KEY")


def pipeline_init(**kwargs):
    if kwargs["model"] in OPENAI_MODELS:
        return kwargs["pipeline_class"](**kwargs)
    else:
        return transformers.pipeline(**kwargs)

# class Record(DictConfig):
#     def __init__(self, generated_sequence=None,
#                  seq_log_prob=0,
#                  full_text="",
#                  **kwargs):
#         d = {
#             "generated_sequence": generated_sequence,
#             "seq_log_prob": seq_log_prob,
#             "full_text": full_text
#         }
#         d = dict(**kwargs, **d)
#         super().__init__(d)

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
        if not self.openai:
            super().__init__(*args, **kwargs)
            self._forward_params = {}

        print(args)

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
        filtered_logprob = filtered_logprob_sum / filtered_cnt
        logprob = logprob_sum / cnt
        return {"seq_log_prob_average": logprob, "seq_log_prob_filtered": filtered_logprob}

    def postprocess(self, model_outputs, return_type=ReturnType.NEW_TEXT, clean_up_tokenization_spaces=True):
        generated_sequence = model_outputs["generated_sequence"][0]
        input_ids = model_outputs["input_ids"]
        prompt_text = model_outputs["prompt_text"]
        scores = model_outputs["scores"]
        tokens_probs_list = [[(self.tokenizer.decode(token), torch.exp(score).item())
                              for score, token in zip(scores[i], generated_sequence[i][-len(scores[i]):])] for i in range(len(scores))]

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
                record = {"generated_text": all_text, "seq_log_prob": seq_log_probs[i].item(), "full_text": full_text, "output": all_text}
                log_probs = self.post_process_cal_logprob(tokens_probs_list[i])
                record.update(log_probs)
                record = Record(**record)
            records.append(record)

        return records
    @retry((Timeout, APIError,ServiceUnavailableError), tries=5, delay=1, backoff=2, max_delay=4)
    def get_openai_completion(self, prompt, temperature=0):
        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,)
        output = response.choices[0].message["content"]

        record = Record({"generated_text": output,
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

    def __call__(self, inputs, *args, temperature=0, num_workers=None, batch_size=None, **kwargs):
        if self.openai:
            return self.get_openai_completion(inputs, temperature=temperature)
        else:
            records = super().__call__(inputs, **kwargs)
            return records

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0, **kwargs):
        output = {}
        return output


SELF_EVAL_TEMPLATE_CHAT = '''<s>[INST] You will be given a question and your own answer to the question. Please evaluate your own answer and provide a score from 0-100. After that, provide your confidence score about your evaluation.

Question: {question}

Your answer: {answer}

Now please provide your score about this answer in the format of "Correctness Score: <Your score>/100" and give your explanation. After that, provide your confidence about your evaluation in the format of "Confidence Score: <Your score>/100" and give your explanation.[/INST]
'''


class SelfEvalPipeline(MyPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "chat" in self.model_name:
            self.template = SELF_EVAL_TEMPLATE_CHAT
        else:
            raise Exception

    def fit_template(self, answer, question=""):
        prompt = self.template.format(question=question, answer=answer)
        # print(prompt)
        return prompt

    def extract_scores(self, text):
        correctness_score = self.extract_score(text, pattern=r"Correctness Score: (\d+)/100")
        confidence_score = self.extract_score(text, pattern=r"Confidence Score: (\d+)/100")
        return correctness_score, confidence_score

    def extract_confidence_score(self, answer, question, dataset_name="asqa", temperature=0, **kwargs):
        inputs = self.fit_template(answer=answer, question=question)
        outputs = self.__call__(inputs, temperature=temperature, **kwargs)
        comment = outputs[0]["generated_text"]
        correctness_score, confidence_score = self.extract_scores(comment)

        output = {
            "inputs_self_eval": inputs,
            "comment_self_eval": comment,
            "correctness_score_self_eval":  correctness_score,
            "confidence_score_self_eval": confidence_score
        }
        return output




GRADER_TEMPLATE = '''{task_instruction}

{grader_instruction}

Question: {question}

Gold Answer: {gold_answer}

Student's answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/100" and give your explanation.
'''
FACT_GRADER_TEMPLATE = '''You will be given a student's answer and please evaluate the answer for its factuality.

Student's answer: {answer}

Now please provide your score about this answer in the format of "Score: <Your score>/100" and give your explanation.
'''


class GraderPipeline(MyPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grader_template = GRADER_TEMPLATE
        self.fact_grader_template = FACT_GRADER_TEMPLATE
        self.grader_instruction = "You will be given a question, a gold answer, and a student's answer. Please evaluate the student's answer based on the gold answer, and provide a score from 0-100 to the student's answer."
        self.asqa_instruction = "Given an ambiguous factoid question that has different correct answers depending on interpretation, the answer should be a long-form summary that resolves the ambiguity. "

    def fit_template(self, answer, question="", gold_answer="", eval_fact=False):
        if not eval_fact:
            prompt = self.grader_template.format(task_instruction=self.asqa_instruction,
                                                 grader_instruction=self.grader_instruction,
                                                 question=question,
                                                 gold_answer=gold_answer,
                                                 answer=answer)
        else:
            prompt = self.fact_grader_template.format(answer=answer)
        # print(prompt)
        return prompt


    def evaluate_answer(self, answer, question, gold_answer, dataset_name="asqa", temperature=0, **kwargs):
        inputs = self.fit_template(answer=answer, question=question, gold_answer=gold_answer, eval_fact=False)
        outputs = self.__call__(inputs, temperature=temperature, **kwargs)
        comment = outputs[0]["generated_text"]
        score = self.extract_score(comment)

        fact_inputs = self.fit_template(answer=answer, eval_fact=True)
        outputs = self.__call__(fact_inputs, temperature=temperature, **kwargs)
        fact_comment = outputs[0]["generated_text"]
        fact_score = self.extract_score(fact_comment)

        output = {
            "inputs_grader": inputs,
            "comment": comment,
            "score": score,
            "fact_inputs_grader": fact_inputs,
            "fact_comment": fact_comment,
            "fact_score": fact_score
        }
        return output


