from typing import Optional

import fire

from llama import Llama

import time
import argparse

import pandas as pd
import numpy as np
import json

from tqdm import tqdm
from typing import List, Optional

def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 150,
    max_batch_size: int = 4,
    messages = list,
    max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    results = generator.chat_completion(
        messages,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    # for message, result in zip(messages, results):
    #     for msg in message:
    #         print(f"{msg['role'].capitalize()}: {msg['content']}\n")
    #     print(
    #         f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
    #     )
    #     print("\n==================================\n")
    for result in results:
        return result['generation']['content']





if __name__ == "__main__":
    df = pd.read_csv('/usr/xtmp/qz124/misinfo_vax_ss23/llama/pilot_0728_generate_attribute_Finalized.csv')
    all_mes = []
    # temp check
    mes = df['A_prompt_openai'][0]
    if isinstance(mes, str):
        mes = eval(mes)
    assert isinstance (mes, list)

    print("prompt:", mes)
    ckpt_dir = "/usr/xtmp/qz124/misinfo_vax_ss23/llama/llama-2-7b-chat"
    tokenizer_path = "/usr/xtmp/qz124/misinfo_vax_ss23/llama/tokenizer.model"
    print(mes)
    mes = "Hello alpaca"
    response = main(messages=[mes], ckpt_dir=ckpt_dir, tokenizer_path=tokenizer_path)
    print(response)



