import pandas as pd
import transformers
import torch
import fire
import os
import json
import numpy as np

from pipeline import (MyPipeline, OPENAI_MODELS, pipeline_init,
                      SelfEvalRepetitionPipeline, SelfEvalRangePipeline,
                      SelfVerificationPipeline,
                      SelfRepetitionPipeline, SelfRepetitionSplitPipeline,
                      SelfRepetitionNERPipeline, SelfRepetitionClaimPipeline,
                      RephraseConsistencyPipeline)
from transformers import AutoTokenizer
from peft import AutoPeftModelForCausalLM
from omegaconf import OmegaConf
from utils import make_head_prompt, DATASET_PROFILES
from tqdm import tqdm
from prompter import Prompter

import sys
import logging


def main(
        config_path="configures/v1.0.0.yml"
):
    args = OmegaConf.load(config_path)

    print(args)
    model = args.model
    model_name = args.model.split("/")[-1]

    if args.get("model_path", None) is not None:
        model = AutoPeftModelForCausalLM.from_pretrained(args.model_path, torch_dtype=torch.bfloat16, device_map="auto")
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
    else:
        tokenizer = AutoTokenizer.from_pretrained(model) if model not in OPENAI_MODELS else None


    eos_token_id = tokenizer.eos_token_id if model not in OPENAI_MODELS else 0
    confidence_method = args.get("confidence_method", "")
    confidence_to_pipeline = {
        "": MyPipeline,
        "self_verification": SelfVerificationPipeline,
        # "self_eval": SelfEvalPipeline,
        "self_eval_repetition": SelfEvalRepetitionPipeline,
        "self_eval_range": SelfEvalRangePipeline,
        "log_prob": MyPipeline,
        "self_repetition": SelfRepetitionPipeline,
        "self_repetition_split": SelfRepetitionSplitPipeline,
        "self_repetition_ner": SelfRepetitionNERPipeline,
        "self_repetition_claim": SelfRepetitionClaimPipeline,
        "rephrase_consistency": RephraseConsistencyPipeline,
    }

    num_return_sequences = args.get("num_return_sequences", 1)

    pipeline = pipeline_init(
        task="text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
        pipeline_class=confidence_to_pipeline[confidence_method],
        model_name=model_name,
        tokenizer=tokenizer,
    )

    # set seed
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    # Load data
    # prompt_data = json.load(open(args.prompt_file))
    prompt_data = DATASET_PROFILES[args.dataset_name]
    do_n_doc = True if args.n_doc > 0 else False

    eval_data = json.load(open(args.eval_file))
    if args.get("answer_file", None) is not None:
        eval_data = pd.read_json(args.answer_file)['data'].to_list()


    if args.sample_num > 0:
        if args.get("sample_start", None) is not None:
            eval_data = eval_data[args.sample_start: args.sample_start + args.sample_num]
            print(f"sample from {args.sample_start} to {args.sample_start + args.sample_num}")
        else:
            eval_data = eval_data[:args.sample_num]
    else:
        args.sample_num = len(eval_data)

    prompter_ = Prompter(prompt_data=prompt_data,
                        n_shot=args.n_shot,
                        n_doc=args.n_doc,
                        n_doc_in_demo=args.n_doc_in_demo,
                        fewer_doc_in_demo=args.fewer_doc_in_demo,
                        no_doc_in_demo=args.no_doc_in_demo,
                        use_shorter=args.use_shorter,
                        dataset_name=args.dataset_name,
                        model_name=args.model,
                         oracle_doc=args.get("oracle_doc", False),
                        )

    for idx, eval_item in tqdm(enumerate(eval_data)):
        text_input = prompter_.generate_text_input(task_type="main",
                                                   eval_item=eval_item,)

        eval_data[idx]['text_input'] = text_input

        if idx == 0:
            print(text_input)
        if args.get("answer_file", None) is None:
            sequences = pipeline(
                text_input,
                do_sample=True,
                top_k=10,
                num_return_sequences=num_return_sequences,
                eos_token_id=eos_token_id,
                # max_length=2048,
                max_new_tokens=2048,
                random_state=args.seed
            )

            eval_item.update(sequences[0])
            other_answers = [item["generated_text"] for item in sequences[1:]]
            eval_item["other_answers"] = other_answers
        else:
            other_answers = None

        confidence_output = pipeline.extract_confidence_score(answer=eval_item["generated_text"],
                                                              question=eval_item["question"] if "question" in eval_item else None,
                                                              dataset_name=args.dataset_name,
                                                              other_answers=other_answers,
                                                              eval_item=eval_item,
                                                              n_doc=0 if not do_n_doc else args.n_doc,
                                                              oracle_doc=args.get("oracle_doc", False),
                                                              )
        eval_item.update(confidence_output)

    save_dir = os.path.join(args.save_dir, f"results/{args.exp_name}/{args.dataset_name}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"create {save_dir}")
    if args.get("sample_start", None) is not None:
        save_path = os.path.join(save_dir, f"{model_name}_predictions_{args.sample_start}_{args.sample_start + args.sample_num}.json")
    else:
        save_path = os.path.join(save_dir, f"{model_name}_predictions_{args.sample_num}.json")

    with open(save_path, 'w') as f:
        json.dump(eval_data, f)
        print(f"save to {save_path}")

if __name__ == '__main__':
    fire.Fire(main)