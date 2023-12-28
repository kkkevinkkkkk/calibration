This directory contains data examples in the CNN/DailyMail dataset: https://huggingface.co/datasets/cnn_dailymail.

Since recent work has found that the original reference summaries in CNN/DM are not as good as LLM-generated summaries, we provide the GPT-4 generated summaries instead.

The articles are preprocessed to be around 1024 tokens long, and the summaries are always 3-sentence long to mimic the original CNN/DM summaries. The average summary length is around 100 tokens.

There are 1000 examples sampled from the original training set, and 100 examples sampled from the original validation and test sets.
The two attributes are "article" and "summary" for each example.

*Warning*: we have seen that sometimes (~2-3% of times) Llama-2 models can refuse to generate a summary for a given article because of ethical concerns. Usually sampling multiple times will solve the issue.