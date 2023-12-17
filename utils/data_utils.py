import pandas as pd
import os
df = pd.read_json("/usr/xtmp/yh386/calibration/results/train/asqa/Llama-2-13b-chat-hf_predictions_4353.json")
df = pd.read_json("/usr/xtmp/yh386/calibration/results/run/asqa/Llama-2-70b-chat-hf_predictions_100.json")
df

save_dir = "/usr/xtmp/yh386/calibration/results/train/asqa"
model_to_result_paths = {
    "vicuna-13b": "vicuna-13b-v1.3_predictions_4353.json",
    "llama-2-13b": "Llama-2-13b-chat-hf_predictions_4353.json",
    "llama-2-70b": "Llama-2-70b-chat-hf_predictions_4353.json",
    "gpt-3.5-turbo": "gpt-3.5-turbo_predictions_0_200.json",
    "llama-2-7b": "Llama-2-7b-chat-hf_predictions_4353.json",
}
model_to_range_v1 = {
    "vicuna-13b": (1000, 1200),
    "llama-2-13b": (2000, 2200),
    "llama-2-70b": (3000, 3200),
    "gpt-3.5-turbo": (0, 200),
    "llama-2-7b": (4000, 4200),
}
model_to_range_v2 = {
    "vicuna-13b": (1200, 1400),
    "llama-2-13b": (2200, 2400),
    "llama-2-70b": (3200, 3400),
    # "gpt-3.5-turbo": (200, 400),
    "llama-2-7b": (200, 600),
}
model_to_range_dict = {
    "v1": model_to_range_v1,
    "v2": model_to_range_v2,
}

version = "v2"

model_to_range = model_to_range_dict[version]
model_to_result_paths = {key: os.path.join(save_dir, value) for key, value in model_to_result_paths.items()}
df_total = []
for name in model_to_range.keys():
    result_path = model_to_result_paths[name]
    df = pd.read_json(result_path)
    df = df[model_to_range[name][0]:model_to_range[name][1]]
    if "id" not in df.columns:
        df["id"] = df.index
    df["model"] = name
    print(name, len(df))
    df_total.append(df)
df_total = pd.concat(df_total)
df_total.sort_values(by="id", inplace=True)
df_total.to_json(os.path.join(save_dir, f"all_predictions_{version}.json"), orient="records")
print(len(df_total))


from collections import defaultdict
from sklearn.model_selection import train_test_split
model_to_range_merged = defaultdict(list)
train_version = "v1.0"
data_versions = ["v1", "v2"]
df_total = []
df_total_scored = []
for version in data_versions:
    model_to_range_ = model_to_range_dict[version]
    for model, model_range in model_to_range_.items():
        model_to_range_merged[model] += list(range(model_range[0], model_range[1]))

    df_total += pd.read_json(os.path.join(save_dir, f"all_predictions_{version}.json"), orient="records").to_dict(orient="records")
    df_total_scored += pd.read_json(os.path.join(save_dir, f"all_predictions_{version}.json.qa_gpt-4_five_pnt_t:0.7.score"), orient="records")['data'].to_list()
df_total = pd.DataFrame(df_total)
df_total_scored = pd.DataFrame(df_total_scored)
df_train, df_val = train_test_split(df_total_scored, test_size=0.1, random_state=42)
df_train.to_json(os.path.join(save_dir, f"train_{train_version}.json"), orient="records")
df_val.to_json(os.path.join(save_dir, f"val_{train_version}.json"), orient="records")
