import fire
import os
import pandas as pd
from utils import analyze, read_predictions_and_results


def main(dataset_name: str = "asqa",  # "asqa", "eli5", "qampari", "cnndm"
         model_name: str = "Llama-2-13b-chat-hf",  # "Llama-2-13b-chat-hf", "vicuna-13b-v1.3", "gpt-3.5-turbo"
         confidence_method="self_eval_repetition",
         # "self_eval_repetition", "self_repetition_claim",
         # "self_repetition", "self_repetition_ner", "self_repetition_split"
         sample_start=None,
         sample_num=500,
         result_dir="./results"):
    '''
        :param dataset_name: the name of the dataset
        :param model_name: the name of the model
        :param confidence_method: the confidence extraction method
        :param sample_start: the beginning index of the data
        :param sample_num: the number of data
        :param result_dir: the directory of the results
        :return:
    '''

    df_merged, scores = read_predictions_and_results(dataset_name=dataset_name,
                                                     confidence_method=confidence_method,
                                                     model_name=model_name,
                                                     sample_start=sample_start,
                                                     sample_num=sample_num,
                                                     result_dir=result_dir)

    print("***************Performance***************")
    for k, v in scores.items():
        print(f"{k}: {round(v, 2)}")

    calibration_results = analyze(df_merged, score_threshold=0.8)
    print("\n\n***************Calibration***************")
    for k, v in calibration_results.items():
        print(f"{k}: {round(v, 3)}")
    return


if __name__ == "__main__":
    fire.Fire(main)
