from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from math import ceil
from scipy.stats import wasserstein_distance

def print_info(item, self_eval=False, gpt_eval=False):
    print("************Question**********")
    print(item["text_input"])
    print("************Gold Answer**********")
    print(item["answer"])
    print("************Answer**********")
    print(item["output"])
    if self_eval:
        print()
        print("************inputs for self-evaluation**********")
        print(item['inputs_self_eval'])
        print("************self-evaluation comments**********")
        print(item['comment_self_eval'])
        print("************correctness score for self-evaluation**********")
        print(item['correctness_score_self_eval'])
        print("************confidence score for self-evaluation**********")
        print(item['confidence_score_self_eval'])

    if gpt_eval:
        print("************GPT-3.5 Fact comment**********")
        print(item["gpt-3.5-turbo_fact_comment"])
        print("************GPT-3.5 Comment**********")
        print(item["gpt-3.5-turbo_comment"])
        print("************Fact comment**********")
        print(item["gpt-4_fact_comment"])
        # print(item["gpt-4_fact_score"])
        print("************Comment**********")
        print(item["gpt-4_comment"])
        # print(item["gpt-4_score"])
        # for i in range(5):
        #     print(data[data_idx][f'gpt-3.5-turbo_score_{i}'])
        #     print(data[data_idx][f'gpt-3.5-turbo_fact_score_{i}'])
        #     print(data[data_idx][f'gpt-3.5-turbo_fact_comment_{i}'])
        # for k, v in item.items():
        #     if "gpt-4" in k:
        #         print(f"{k}: {v}")

    print("\n\n\n")

def df_column_switch(df, column1, column2):
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df = df[i]
    return df


def compare_diff(scores1, scores2):
    diff = [s1 - s2 for s1, s2 in zip(scores1, scores2)]
    diff = np.array(diff)
    max_indices = np.argsort(diff)[:3]
    min_indices = np.argsort(diff)[-3:][::-1]

    print(diff[max_indices], max_indices, diff[min_indices], min_indices)

def get_dataframe(data, column_names=None, data_indices=None, post_process=False):
    df_out = defaultdict(list)
    data_indices = list(range(len(data))) if data_indices is None else data_indices
    column_names = data[0].keys() if column_names is None else column_names

    for data_idx in data_indices:
        df_out["idx"].append(data_idx)
        for column_name in column_names:
            if column_name in ["QA-F1", "QA-EM"]:
                df_out[column_name].append(round(100 * data[data_idx][column_name],1))
            else:
                df_out[column_name].append(data[data_idx][column_name])

    df_out = pd.DataFrame(df_out)
    df_out = df_out.round(1)

    if post_process:
        df_out = postprocess(df_out)
    return df_out

def postprocess(df_out):
    df_out["gpt-4_score"] = df_out.apply(lambda row: str(row["gpt-4_score"]) + "\u00B1" + str(row["gpt-4_score_std"]),
                                         axis=1)
    df_out["gpt-4_fact_score"] = df_out.apply(
        lambda row: str(row["gpt-4_fact_score"]) + "\u00B1" + str(row["gpt-4_fact_score_std"]), axis=1)
    df_out["gpt-3.5-turbo_score"] = df_out.apply(
        lambda row: str(row["gpt-3.5-turbo_score"]) + "\u00B1" + str(row["gpt-3.5-turbo_score_std"]), axis=1)
    df_out["gpt-3.5-turbo_fact_score"] = df_out.apply(
        lambda row: str(row["gpt-3.5-turbo_fact_score"]) + "\u00B1" + str(row["gpt-3.5-turbo_fact_score_std"]), axis=1)
    df_out = df_out.drop(
        ["gpt-4_score_std", "gpt-4_fact_score_std", "gpt-3.5-turbo_score_std", "gpt-3.5-turbo_fact_score_std"], axis=1)

    return df_out


def split_sentence(words, probs, max_words_per_line):
    lines = [words[i:i + max_words_per_line] for i in range(0, len(words), max_words_per_line)]
    probs_lines = [probs[i:i + max_words_per_line] for i in range(0, len(words), max_words_per_line)]
    return lines, probs_lines


def display_sentence_with_colors(words, probs, max_words_per_line=15):
    lines, probs_lines = split_sentence(words, probs, max_words_per_line)

    fig, ax = plt.subplots()
    for line_index, line in enumerate(lines):
        alphas = [prob * 0.95 + 0.05 for prob in probs_lines[line_index]]
        for word_index, (word, alpha) in enumerate(zip(line, alphas)):
            ax.text(word_index, -line_index, word, color="#000000", size=60, alpha=alpha)

    ax.axis('off')
    plt.show()

def extract_confidence_distribution(scores, category_num=6):
    confidence_distribution = [0] * category_num
    score_interval = 100 / (category_num - 1)
    for score in scores:
        if np.isnan(score):
            score = 0
        confidence_distribution[int(round(score / score_interval))] += 1 / len(scores)
    confidence_distribution = [round(confidence_distribution[i], 3)for i in range(category_num)]
    return confidence_distribution

def extract_confidence_distribution_lambda(row, confidence_method="self_eval_repetition"):
    if confidence_method == "self_eval_repetition":
        scores = row["scores_self_eval"]
    elif confidence_method == "self_repetition":
        scores = [row[f"score_repetition{j}"] for j in range(9)]
    elif confidence_method == "self_repetition_split":
        scores = [row[f"score_repetition_split{j}"] for j in range(9)]
    elif confidence_method == "self_repetition_ner":
        scores = row['scores_repetition_ner']
    elif confidence_method == "self_repetition_claim":
        scores = row['scores_repetition_claim']
    else:
        raise NotImplementedError
    return extract_confidence_distribution(scores)

def read_predictions_and_results(
        dataset_name="asqa",
        confidence_method="self_eval_repetition",
        model_name="Llama-2-13b-chat-hf",
        path="/usr/xtmp/yh386/calibration/results", ):

    predictions_path_template = "{confidence_method}/{dataset_name}/{model_name}_predictions_100.json"
    result_path_template = "run/{dataset_name}/{model_name}_predictions_100.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"

    if dataset_name == "asqa":
        task_metric = "qa"
    elif dataset_name == "eli5":
        task_metric = "claims_nli"
    else:
        raise NotImplementedError

    predictions_path = predictions_path_template.format(confidence_method=confidence_method,
                                                        dataset_name=dataset_name,
                                                        model_name=model_name)
    predictions_path = os.path.join(path, predictions_path)
    result_path = result_path_template.format(dataset_name=dataset_name,
                                                model_name=model_name,
                                                task_metric=task_metric)
    result_path = os.path.join(path, result_path)

    score_column_map = {
        "self_repetition": "score_repetition",
        "self_repetition_split": "score_repetition_split",
        "self_repetition_ner": "score_repetition_ner",
        "self_repetition_claim": "score_repetition_claim",
        "self_verification": "score",
        "self_eval_repetition": "score_self_eval",
        "self_eval_range": "score",
    }


    with open(predictions_path, 'r') as f:
        predictions = json.load(f)
        print(f"load predictions from {predictions_path}")

    df_pred = pd.DataFrame(predictions)

    with open(result_path, 'r') as f:
        print(f"load result from {result_path}")
        data_w_scores = json.load(f)
        scores = {k: v for k, v in data_w_scores.items() if k != "data"}
        data = data_w_scores["data"]

    df_data = pd.DataFrame(data)
    if "gpt-4_scores" not in df_data.columns:
        df_data["gpt-4_scores"] = df_data.apply(lambda row: [row[f'gpt-4_score_{i}'] for i in range(5)], axis=1)
    confidence_distributions = []
    for gpt4_scores in df_data["gpt-4_scores"]:
        confidence_distribution = extract_confidence_distribution(gpt4_scores)
        confidence_distributions.append(confidence_distribution)
    df_data["gpt-4_confidence_distribution"] = confidence_distributions
    print(scores)

    df_pred["confidence_distribution"] = df_pred.apply(
        lambda row: extract_confidence_distribution_lambda(row, confidence_method),
        axis=1)

    assert score_column_map[confidence_method] in df_pred.columns
    df_pred = df_pred.rename(columns={score_column_map[confidence_method]: "score"})

    return df_pred, df_data, scores

def selective_answering_distributed(confidence_distributions, conf_threshold=1, score_threshold=1):
    category_num = len(confidence_distributions[0])
    score_interval = 1 / (category_num - 1)
    total_select = []
    for confidence_distribution in confidence_distributions:
        conf_score = 0
        for i in range(ceil(score_threshold / score_interval), category_num):
            conf_score += confidence_distribution[i]
        select = True if conf_score >= conf_threshold else False
        total_select.append(select)
        # print(confidence_distribution, conf_score, select)
    return total_select
def selective_answering_singular(scores, score_threshold=0.6):
    total_select = []
    for score in scores:
        select = True if round(score/100,2) >= score_threshold else False
        total_select.append(select)
    return total_select

def selective_answering_analyze(df_pred, df_data):
    df_distributed_calibration = []
    for conf_threshold in [0.6, 0.8, 1.0]:
        l = {}
        for score_threshold in [0.6, 0.8, 1.0]:
            total_select = selective_answering_distributed(df_pred["confidence_distribution"], conf_threshold,
                                                           score_threshold)
            select_num, score = np.sum(total_select), np.mean((df_data[total_select]["gpt-4_score"]))
            covered_num = np.sum(np.array(df_data["gpt-4_score"] >= 100*score_threshold) & np.array(total_select))
            total_num = np.sum(np.array(df_data["gpt-4_score"] >=100 *score_threshold))

            precision = covered_num / select_num
            recall = covered_num / total_num
            f1 = round(2 * precision * recall / (precision + recall), 2)

            result = f"{round(score, 2)}({covered_num}/{select_num})({covered_num}/{total_num})({f1})"
            l[score_threshold] = result
        # df_distributed_calibration[conf_threshold] = l
        df_distributed_calibration.append(l)
    df_distributed_calibration = pd.DataFrame(df_distributed_calibration)
    df_distributed_calibration.index = [0.6, 0.8, 1.0]
    print(df_distributed_calibration)
    print()

    df_singular_calibration = [{}]
    for conf_threshold in [0.6, 0.8, 1.0]:
        total_select = selective_answering_singular(df_pred["score"], conf_threshold)
        select_num, score = np.sum(total_select), np.mean((df_data[total_select]["gpt-4_score"]))
        covered_num = np.sum(np.array(df_data["gpt-4_score"] >= 100 * conf_threshold) & np.array(total_select))
        total_num = np.sum(np.array(df_data["gpt-4_score"] >= 100 * conf_threshold))
        precision = covered_num / select_num
        recall = covered_num / total_num
        f1 = round(2 * precision * recall / (precision + recall), 2)
        result = f"{round(score, 2)}({covered_num}/{select_num})({covered_num}/{total_num})({f1})"
        df_singular_calibration[0][conf_threshold] = result
    df_singular_calibration = pd.DataFrame(df_singular_calibration)
    print(df_singular_calibration)
    print()



def analyze(
        df_pred, df_data):
    selective_answering_analyze(df_pred, df_data)
    score_columns = ["gpt-4_score"]

    similarity_scores = []
    for i in range(len(df_pred)):
        distribution1 = df_pred["confidence_distribution"][i]
        distribution2 = df_data["gpt-4_confidence_distribution"][i]
        distance = wasserstein_distance(range(6), range(6), distribution1, distribution2) / 5
        # print(distribution1, distribution2, distance)
        similarity = 1 - distance
        similarity_scores.append(similarity)

    print()
    print("wasserstein_distance similarity")
    print(round(np.mean(similarity_scores), 2))

    df_score = pd.concat([df_data[score_columns], df_pred["score"]], axis=1)
    print("correlation")
    print(df_score.corr())
    print()
    return similarity_scores