# Calibration
## Calibrating Long-form Generations from Large Language Models

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)]()

This is the repository of source code for our paper "Calibrating Long-form Generations from Large Language Models". The paper can be found at [arXiv](https://arxiv.org/abs/2402.06544).

## Table of Contents
   - [Install](#install)
     - [Packages](#packages)
     - [Data](#data)
   - [Run](#run)
   - [Evaluation](#evaluation)
   - [Analysis](#analysis)

   <!-- - [Authors](#authors) -->

## Install

### Packages
The first things you need to do are cloning this repository and installing its
dependencies:

```sh
git clone hhttps://github.com/kkkevinkkkkk/calibration.git
cd calibration
pip install -r requirements.txt
```

### Data
The data used in this project is from ASQA, QAMAPRI, ELI5, CNNDM. A demo dataset is in [datasets/asqa_eval_examples.json](datasets/asqa_eval_examples.json). 
You could download the full datasets from the `data` folder in this [link](https://drive.google.com/drive/folders/1Egd8Kij4XyhI0lxtBViSCHOMoxIjh1sQ?usp=sharing)

## Run
Configure files of running the models are in [configures/](configures). You could change the settings by changing the corresponding `.yml` file.

A demo configure file is in [configures/v0.0.0.yml](configures/v0.0.0.yml). With this configure, you are running a Llama-2-7b-chat on asqa dataset without any confidence extraction method. 

You could run the demo by:
```sh
bash scripts/run.sh
```

To run confidence extraction method, you could change the `confidence_method` in the configure file. 
There are five different confidence extraction methods: 
1. `self_eval_repetition` 
2. `self_repetition` 
3. `self_repetition_claim` 
4. `self_repetition_ner` 
5. `self_repetition_split`

See [configures/v0.0.1.yml](configures/v0.0.1.yml) and [configures/v0.0.2.yml](configures/v0.0.2.yml) for examples.
All `self-repetition` corresponds to the `self-consistency`methods in the paper.



Predictions file will be saved in [results/](results) by default. You could change the output path by changing the `save_dir` in the configure file.
The default result path follows the template `results/{confidence_method}/{dataset}/{model_name}_predictions_{sample_num}.json`.
The confidence method will be set to `run` if you don't use any.

## Evaluation
To evaluate the correctness of model predictions with GPT-4, you need to first export the openai api key to environment variable `OPENAI_API_KEY`. Then run the following command:

```sh
bash scripts/eval.sh
```
You could change the model predictions by change `RESULT_PATH` in [scripts/eval.sh](scripts/eval.sh). The default model predictions is in [results/run/asqa/Llama-2-7b-chat-hf_predictions_5.json](results/run/asqa/Llama-2-7b-chat-hf_predictions_5.json)
> Note: for `ASQA` and `ELI5`, we not only measure the gpt-4 score but also measure the task metrics. So it requires GPU to run the evaluation.


## Analysis
To analyze the results, you could run the following command for demo usage:

```sh
bash scripts/analysis.sh
```
To reproduce the results in the paper, you need to first download our results from `results` in this [link](https://drive.google.com/drive/folders/1Egd8Kij4XyhI0lxtBViSCHOMoxIjh1sQ?usp=sharing) and use it to overwrite the `results` folder. 

Then you need to change the `DATASET_NAME`, `MODEL_NAME`, `CONFIDENCE_METHOD`, `SAMPLE_NUM` in [scripts/analysis.sh](scripts/analysis.sh) to reproduce the results in the paper.








