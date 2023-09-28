import transformers
import torch
import fire
import os
import json
import numpy as np

from pipeline import MyPipeline, OPENAI_MODELS, pipeline_init
from transformers import AutoTokenizer
from omegaconf import OmegaConf
from utils import make_demo, make_head_prompt, make_text_input
from tqdm import tqdm


def main(
        config_path="configures/v1.0.0.yml"
):
    args = OmegaConf.load(config_path)

    print(args)
    model = args.model

    tokenizer = AutoTokenizer.from_pretrained(model) if model not in OPENAI_MODELS else None
    eos_token_id = tokenizer.eos_token_id if model not in OPENAI_MODELS else 0

    pipeline = pipeline_init(
        task="text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
        pipeline_class=MyPipeline,
    )

    # Generate prompts
    np.random.seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    # Load data
    prompt_data = json.load(open(args.prompt_file))
    eval_data = json.load(open(args.eval_file))

    if args.sample_num > 0:
        eval_data = eval_data[:args.sample_num]
    else:
        args.sample_num = len(eval_data)



    head_prompt = make_head_prompt(prompt_data,
                                   n_shot=args.n_shot,
                                   n_doc=args.n_doc,
                                   n_doc_in_demo=args.n_doc_in_demo,
                                   fewer_doc_in_demo=args.fewer_doc_in_demo,
                                   no_doc_in_demo=args.no_doc_in_demo,
                                   use_shorter=args.use_shorter,)

    for idx, eval_item in tqdm(enumerate(eval_data)):
        text_input = make_text_input(eval_item,
                                     head_prompt=head_prompt,
                                     model_name=args.model,
                                     n_doc=args.n_doc,
                                     template=prompt_data["demo_prompt"],
                                     doc_prompt=prompt_data["doc_prompt"],
                                     instruction=None,
                                     use_shorter=args.use_shorter,
                                     test=True,
                                     dataset_name=args.dataset_name)

        eval_data[idx]['text_input'] = text_input
        # eval_data[idx]['prompt'] = text_input

        if idx == 0:
            print(text_input)

        sequences = pipeline(
            text_input,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=eos_token_id,
            max_length=2048,
        )

        eval_item["output"] = sequences[0]["generated_text"]
        eval_item["seq_log_prob"] = sequences[0]["seq_log_prob"]

        # eval_item['output'] = output_array if len(output_array) > 1 else output_array[0]

    model_name = args.model.split("/")[-1]
    save_dir = os.path.join(args.save_dir, f"results/{args.exp_name}/{args.dataset_name}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"create {save_dir}")
    save_path = os.path.join(save_dir, f"{model_name}_predictions_{args.sample_num}.json")

    with open(save_path, 'w') as f:
        json.dump(eval_data, f)
        print(f"save to {save_path}")


if __name__ == '__main__':
    fire.Fire(main)