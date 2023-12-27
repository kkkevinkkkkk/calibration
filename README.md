# calibration
## Unifying Calibration Measurement: A General System for Evaluating LLMs Reliability

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)]()

This is the repository of source code for our paper "Unifying Calibration Measurement: A General System for Evaluating LLMs Reliability".

## Table of Contents
   - [Install](#install)
   - [Run](#run)
     - [Full-model Tuning](#full-model-tuning)
     - [Prompt Tuning](#prompt-tuning)
     - [Pre-trained Prompt Tuning](#pre-trained-prompt-tuning)
   - [Evaluation](#evaluation)

   <!-- - [Authors](#authors) -->

## Install

The first things you need to do are cloning this repository and installing its
dependencies:

```sh
git clone hhttps://github.com/kkkevinkkkkk/calibration.git
cd calibration
pip install -r requirements.txt
```

## Run
Configure files are in [configures/](configures). You could change the settings by changing the corresponding `.yml` file.

A demo configure file is in [configures/v0.0.0.yml](configures/v0.0.0.yml). With this configure, you are running a Llama-2-7b-chat on asqa dataset without any confidence extraction method. 

You could run the demo by:
```sh
bash scripts/run.sh
```

Result file will be saved in [results/](results) by default. You could change the output path by changing the `save_dir` in the configure file.

## Evaluation

You could get the model predictions produced in previous step with GPT-4 by running:
```sh
bash scripts/eval.sh
```
You could change the model predictions by change `RESULT_PATH` in [scripts/eval.sh](scripts/eval.sh). The default model predictions is in [results/run/asqa/Llama-2-7b-chat-hf_predictions_1.json](results/run/asqa/Llama-2-7b-chat-hf_predictions_1.json)









