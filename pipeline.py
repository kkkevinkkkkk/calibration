from transformers import Pipeline, pipeline, TextGenerationPipeline
import torch.nn.functional as F
from transformers.pipelines.text_generation import ReturnType
import torch
import transformers
import openai
import os

OPENAI_MODELS =["gpt-4", "gpt-3.5-turbo"]
openai.api_key = os.getenv("OPENAI_API_KEY")


def pipeline_init(**kwargs):
    if kwargs["model"] in OPENAI_MODELS:
        return MyPipeline(**kwargs)
    else:
        return transformers.pipeline(**kwargs)


class MyPipeline(TextGenerationPipeline):
    def __init__(self, *args, **kwargs):
        self.model_name = kwargs["model"]
        self.openai = True if self.model_name in OPENAI_MODELS else False
        if not self.openai:
            super().__init__(*args, **kwargs)

        print(args)
        print()

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

    def postprocess(self, model_outputs, return_type=ReturnType.NEW_TEXT, clean_up_tokenization_spaces=True):
        generated_sequence = model_outputs["generated_sequence"][0]
        input_ids = model_outputs["input_ids"]
        prompt_text = model_outputs["prompt_text"]
        scores = model_outputs["scores"]
        tokens_probs = [(self.tokenizer.decode(token), torch.exp(score))
                        for score, token in zip(scores[0], generated_sequence[0][-len(scores[0]):])]
        seq_log_prob = torch.sum(scores)

        generated_sequence = generated_sequence.numpy().tolist()
        records = []
        for sequence in generated_sequence:
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

                record = {"generated_text": all_text, "tokens_probs": tokens_probs,
                          "seq_log_prob": seq_log_prob.item(), "full_text": full_text}
            records.append(record)

        return records

    def get_openai_completion(self, prompt, temperature=0):
        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,)
        output = response.choices[0].message["content"]
        records = [{"generated_text": output, "tokens_probs": 0,
                          "seq_log_prob": 0, "full_text": prompt + "\n" + output}]
        return records


    def __call__(self, inputs, *args, num_workers=None, batch_size=None, **kwargs):
        if self.openai:
            return self.get_openai_completion(inputs)
        else:
            records = super().__call__(inputs, **kwargs)
            return records
