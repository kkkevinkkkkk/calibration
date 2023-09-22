from transformers import AutoTokenizer
import transformers
import torch
from pipeline import MyPipeline
import json
import numpy as np
from omegaconf import OmegaConf
from utils import make_demo, make_head_prompt
from tqdm import tqdm
import os

args = OmegaConf.create(
    {"seed": 1,
     "n_shot": 3,
     "n_doc": 0,
     "n_doc_in_demo": 0,
     "no_doc_in_demo": True,
     "fewer_doc_in_demo": False,
     "use_shorter": "summary",
     "dataset_name": "asqa",
     "prompt_file": "templates/asqa_closedbook.json",
     "eval_file": "/usr/xtmp/yh386/datasets/acle/asqa_eval_gtr_top100.json",
     "save_dir": "/usr/xtmp/yh386/calibration"
     })
model = "meta-llama/Llama-2-7b-chat-hf"
model = "gpt2"
model = "meta-llama/Llama-2-7b-hf"



tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
    pipeline_class=MyPipeline,
)

# Generate prompts
np.random.seed(args.seed)
torch.cuda.manual_seed(1)

# Load data
prompt_data = json.load(open(args.prompt_file))
eval_data = json.load(open(args.eval_file))

head_prompt = make_head_prompt(prompt_data,
                               n_shot=args.n_shot,
                               n_doc=args.n_doc,
                               n_doc_in_demo=args.n_doc_in_demo,
                               fewer_doc_in_demo=args.fewer_doc_in_demo,
                               no_doc_in_demo=args.no_doc_in_demo,
                               use_shorter=args.use_shorter)


eval_data = eval_data[:2]
for idx, eval_item in enumerate(eval_data):
    eval_data[idx]['prompt'] = head_prompt + make_demo(
        eval_item, prompt=prompt_data["demo_prompt"], ndoc=args.n_doc, doc_prompt=prompt_data["doc_prompt"],
        instruction=None, use_shorter=args.use_shorter,
        test=True
    )
    text_input = eval_data[idx]['prompt']
    if idx == 0:
        print(text_input)
    sequences = pipeline(
        text_input,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=2048,
    )
    output_array = [sequences]
    eval_item["output"] = sequences[0]["generated_text"]
    eval_item["seq_log_prob"] = sequences[0]["seq_log_prob"].item()

    # eval_item['output'] = output_array if len(output_array) > 1 else output_array[0]

model_name = model.split("/")[-1]
save_dir = os.path.join(args.save_dir, f"predictions/{args.dataset_name}")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print(f"create {save_dir}")
save_path = os.path.join(save_dir, f"{model_name}_predictions.json")

with open(save_path, 'w') as f:
    json.dump(eval_data, f)
    print(f"save to {save_path}")



template = '''<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

You will be given an ambiguous factoid question which have different correct answers depneding on interpretation. Your answer should synthesize factual information from multiple sources into a long-form summary that resolves the ambiguity.
<</SYS>>

Question: {question} [/INST]'''



