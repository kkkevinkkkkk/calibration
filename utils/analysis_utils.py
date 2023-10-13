from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    lines = [' '.join(words[i:i + max_words_per_line]) for i in range(0, len(words), max_words_per_line)]
    probs_lines = [probs[i:i + max_words_per_line] for i in range(0, len(words), max_words_per_line)]
    return lines, probs_lines


def display_sentence_with_colors(words, probs, max_words_per_line=10):
    lines, probs_lines = split_sentence(words, probs, max_words_per_line)
    print(lines)

    fig, ax = plt.subplots()
    for line_index, line in enumerate(lines):
        words = line.split()
        alphas = [prob * 0.9 + 0.1 for prob in probs_lines[line_index]]

        for word_index, (word, alpha) in enumerate(zip(words, alphas)):
            ax.text(word_index, -line_index, word, color="#000000", size=60, alpha=alpha)

    ax.axis('off')
    plt.show()


