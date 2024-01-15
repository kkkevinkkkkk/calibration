from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from math import ceil
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt
from scipy import stats

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
    if confidence_method.startswith("self_eval_repetition"):
        scores = row["scores_self_eval"]
    elif confidence_method == "self_repetition":
        scores = [row[f"score_repetition{j}"] for j in range(9)]
    elif confidence_method == "self_repetition_split":
        scores = [row[f"score_repetition_split{j}"] for j in range(9)]
    elif confidence_method == "self_repetition_ner":
        scores = row['scores_repetition_ner']
        # scores = row['scores_f1']
    elif confidence_method == "self_repetition_claim":
        scores = row['scores_repetition_claim']
    else:
        scores = [row["seq_log_prob"]]
        # print("use seq_log_prob as confidence score")
        # raise NotImplementedError
    return extract_confidence_distribution(scores)

def read_predictions_and_results(
        dataset_name="asqa",
        confidence_method="self_eval_repetition",
        model_name="Llama-2-13b-chat-hf",
        path="/usr/xtmp/yh386/calibration/results",
        sample_num=100,
        sample_start=None,
):
    # trained_model = True if model_name.startswith('5')  else False
    trained_model = True if confidence_method.endswith("trained") else False
    if trained_model and confidence_method == "self_eval_repetition":
        confidence_method = "self_eval_repetition_trained"
    sample_end = sample_start + sample_num if sample_start is not None else sample_num
    sample_num_str = f"{sample_start}_{sample_end}" if sample_start is not None else f"{sample_num}"

    predictions_path_template = "{confidence_method}/{dataset_name}/{model_name}_predictions_{sample_num}.json"

    final_metric = "gpt-4_score"
    if dataset_name == "asqa":
        task_metric = "qa"
    elif dataset_name == "eli5":
        task_metric = "claims_nli"
    elif dataset_name == "qampari":
        task_metric = "qampari_f1_top5"
        final_metric = task_metric
    elif dataset_name == "cnndm":
        task_metric = ""
    else:
        raise NotImplementedError
    if model_name == "gpt-4":
        confidence_method = "run"
    predictions_path = predictions_path_template.format(confidence_method=confidence_method,
                                                        dataset_name=dataset_name,
                                                        model_name=model_name,
                                                        sample_num=sample_num_str)
    predictions_path = os.path.join(path, predictions_path)

    result_path_template = "{exp_name}/{dataset_name}/{model_name}_predictions_{sample_num}.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"
    if trained_model:
        # result_path_template = predictions_path_template.replace("{confidence_method}", confidence_method)
        result_exp_name = "run"
        model_name = "Llama-2-13b-chat-hf"

    else:
        result_exp_name = "run" if "gpt" not in model_name else confidence_method
        if dataset_name == "qampari":
            result_path_template = "{exp_name}/{dataset_name}/{model_name}_predictions_{sample_num}.json.qampari.score"

        elif confidence_method .endswith("_3shot_3doc"):
            confidence_method = confidence_method.replace("_3shot_3doc", "")
            result_path_template = "run_3shot_3doc/{dataset_name}/{model_name}_predictions_{sample_num}.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"
            if "gpt" in model_name:
                result_path_template = "{exp_name}/{dataset_name}/{model_name}_predictions_{sample_num}.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"
        elif confidence_method .endswith("_oracle_doc"):
            confidence_method = confidence_method.replace("_oracle_doc", "")
            result_path_template = "run_oracle_doc/{dataset_name}/{model_name}_predictions_{sample_num}.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"
            if "gpt" in model_name:
                result_path_template = "{exp_name}/{dataset_name}/{model_name}_predictions_{sample_num}.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"
        else:
            if task_metric == "":
                result_path_template = "{exp_name}/{dataset_name}/{model_name}_predictions_{sample_num}.json.gpt-4_five_pnt_t:0.7.score"
            else:
                result_path_template = "{exp_name}/{dataset_name}/{model_name}_predictions_{sample_num}.json.{task_metric}_gpt-4_five_pnt_t:0.7.score"
    result_path = result_path_template.format(dataset_name=dataset_name,
                                              model_name=model_name,
                                              task_metric=task_metric,
                                              sample_num=sample_num_str,
                                              exp_name=result_exp_name)
    result_path = os.path.join(path, result_path)

    score_column_map = {
        "run": "seq_log_prob",
        "self_repetition": "score_repetition",
        "self_repetition_split": "score_repetition_split",
        "self_repetition_ner": "score_repetition_ner",
        # "self_repetition_ner": "score_f1",
        "self_repetition_claim": "score_repetition_claim",
        "self_verification": "score",
        "self_eval_repetition": "score_self_eval",
        "self_eval_range": "score",
        "self_eval_repetition_trained": "score_self_eval",
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
    print(df_data.keys())
    if final_metric == "gpt-4_score":
        if "gpt-4_scores" not in df_data.columns:
            df_data["gpt-4_scores"] = df_data.apply(lambda row: [row[f'gpt-4_score_{i}'] for i in range(5)], axis=1)
        confidence_distributions = []
        for gpt4_scores in df_data["gpt-4_scores"]:
            confidence_distribution = extract_confidence_distribution(gpt4_scores)
            confidence_distributions.append(confidence_distribution)
        df_data["gpt-4_confidence_distribution"] = confidence_distributions
        df_data["correctness_distribution"] = df_data["gpt-4_confidence_distribution"]
        print(scores)
    else:
        df_data["correctness_distribution"] = df_data.apply(
            lambda row: extract_confidence_distribution([row[final_metric]*100]), axis=1)

    df_pred["confidence_distribution"] = df_pred.apply(
        lambda row: extract_confidence_distribution_lambda(row, confidence_method),
        axis=1)

    assert score_column_map[confidence_method] in df_pred.columns
    df_pred = df_pred.rename(columns={score_column_map[confidence_method]: "score"})

    df_pred["confidence_score"] = df_pred["confidence_distribution"].apply(
        lambda x: sum([i / 5 * x[i] for i in range(6)]))
    if final_metric == "gpt-4_score":
        # df_data["expected_correctness"] = df_data["gpt-4_score"] / 100
        df_data["correctness_score"] = df_data["gpt-4_score"] / 100
    else:
        # df_data["expected_correctness"] = df_data[final_metric]
        df_data["correctness_score"] = df_data[final_metric]
    # df_merged = pd.merge(df_pred, df_data, how="inner", on=["question", "answer", "output"])
    df_merged = pd.concat([df_pred, df_data[["correctness_distribution", "correctness_score"]]], axis=1)
    # return df_pred, df_data, scores
    return df_merged, scores
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
        select = True if round(score,2) >= score_threshold else False
        total_select.append(select)
    return total_select

def selective_answering_analyze(df, score_threshold=0.8, conf_threshold=0.8):
    df_distributed_calibration = []
    returned_precision, returned_f1 = 0, 0
    for conf_t in [0.6, 0.8, 1.0]:
        l = {}
        for score_t in [0.4, 0.6, 0.8, 1.0]:
            total_select = selective_answering_distributed(df["confidence_distribution"], conf_t,
                                                           score_t)
            select_num, score = np.sum(total_select), np.mean((df[total_select]["correctness_score"]))
            covered_num = np.sum(np.array(df["correctness_score"] >= score_t) & np.array(total_select))
            total_num = np.sum(np.array(df["correctness_score"] >= score_t))

            precision = covered_num / select_num
            recall = covered_num / total_num
            f1 = round(2 * precision * recall / (precision + recall), 3)

            result = f"{round(score, 2)}({covered_num}/{select_num})({covered_num}/{total_num})({f1})"
            l[score_t] = result
            if score_t == score_threshold and conf_t == conf_threshold:
                returned_precision, returned_f1 = round(precision, 3), round(f1, 3)
        # df_distributed_calibration[conf_threshold] = l
        df_distributed_calibration.append(l)
    df_distributed_calibration = pd.DataFrame(df_distributed_calibration)
    df_distributed_calibration.index = [0.6, 0.8, 1.0]
    print(df_distributed_calibration)
    print()

    return {"precision": returned_precision, "f1": returned_f1}



def analyze(
        df, score_threshold=0.8, conf_threshold=0.8):
    result = selective_answering_analyze(df, score_threshold=score_threshold, conf_threshold=conf_threshold)
    # score_columns = ["gpt-4_score"]
    score_columns = ["correctness_score"]

    confidence = df['confidence_score']
    correctness = df['correctness_score']

    similarity_scores = []
    for i in range(len(df)):
        distribution1 = df["confidence_distribution"][i]
        distribution2 = df["correctness_distribution"][i]
        distance = wasserstein_distance(range(6), range(6), distribution1, distribution2) / 5
        # print(distribution1, distribution2, distance)
        similarity = 1 - distance
        similarity_scores.append(similarity)

    print()
    print("wasserstein_distance similarity")
    print(round(np.mean(similarity_scores), 3))
    wasserstein_similarity = round(np.mean(similarity_scores), 3)
    print()
    print("ece score")
    print(round(np.mean(np.abs(confidence - correctness)), 3))
    print("ece score l2")
    print(round(np.mean(np.square(confidence - correctness)), 3))

    # df_score = pd.concat([df[score_columns], df["confidence_score"]], axis=1)
    df_score = pd.concat([df["correctness_score"], df["score"]], axis=1)
    print("correlation")
    print(df_score.corr())
    print()
    correlation = df_score.corr().iloc[0, 1]


    slope, intercept, r_value, p_value, std_err = stats.linregress(correctness, confidence)
    label_name = f"r={round(r_value, 2)}"
    plt.scatter(correctness, confidence, s=5, label=label_name)
    plt.xlabel("correctness")
    plt.ylabel("confidence")

    result["wasserstein_similarity"] = wasserstein_similarity
    result["ece"] = round(np.mean(np.abs(confidence - correctness)), 3)
    result["correlation"] = correlation

    return result


