from transformers import AutoTokenizer
import transformers
import torch
import json
import fire
from tqdm import tqdm
from utils import get_prompt


def main(
        model="meta-llama/Llama-2-13b-chat-hf",
        dataset_name="asqa",
        ndoc=5,
):


    if dataset_name == "asqa":
        dataset_path = "/usr/xtmp/yh386/datasets/asqa/ASQA.json"
        with open(dataset_path, 'r') as handler:
            eval_data = json.load(handler)["dev"]
    elif dataset_name == "eli5":
        dataset_path = "/usr/xtmp/yh386/datasets/acle/eli5_eval_bm25_top100.json"
        eval_data = json.load(open(dataset_path))
    else:
        raise Exception
        return

    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    torch.cuda.manual_seed(1)

    predictions = {} if dataset_name == "asqa" else eval_data

    eval_iter = eval_data.items() if dataset_name == "asqa" else enumerate(eval_data)
    for idx, eval_item in tqdm(eval_iter):
        prompt = get_prompt(eval_item=eval_item, dataset_name=dataset_name, ndoc=ndoc)
        sequences = pipeline(
            prompt,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            max_length=2048,
        )
        result = sequences[0]['generated_text'].split('[/INST]  ')[-1]

        if dataset_name == "asqa":
            predictions[idx] = result
        else:
            predictions[idx]['output'] = result

    model_name = model.split("/")[-1]
    save_path = f"./datasets/{dataset_name}/predictions/{model_name}_predictions.json"
    with open(save_path, 'w') as f:
        json.dump(predictions, f)
        print(f"save to {save_path}")


if __name__ == '__main__':
    fire.Fire(main)