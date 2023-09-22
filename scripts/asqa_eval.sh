EXP_NAME=Llama-2-13b-chat-hf
#EXP_NAME=t5
PREDICTIONS_PATH=./predictions/${EXP_NAME}_predictions.json
OUTPUT_DIR=./results/${EXP_NAME}
ASQA_PATH=/usr/xtmp/yh386/datasets/asqa/ASQA.json
MODEL_PATH=deepset/roberta-base-squad2
export TRANSFORMERS_CACHE='/usr/xtmp/yh386/.cache/transformers'
export CUDA_VISIBLE_DEVICES='3'
cd datasets/asqa

directory_path=$OUTPUT_DIR

if [ ! -d "$directory_path" ]; then
  mkdir -p "$directory_path"
  echo "Directory $directory_path created along with parent directories as needed."
else
  echo "Directory $directory_path already exists."
fi

filename="${OUTPUT_DIR}/qa.json"
#step 1: convert system output to Roberta input format
python convert_to_roberta_format.py  \
--asqa $ASQA_PATH \
--predictions ${PREDICTIONS_PATH}  \
--split dev \
--output_path ${OUTPUT_DIR}
echo "The file $filename is created."


#step-2 run the roberta squad 2.0 inference
python question-answering/run_qa.py \
  --model_name_or_path $MODEL_PATH \
  --validation_file ${OUTPUT_DIR}/qa.json \
  --do_eval \
  --version_2_with_negative \
  --max_seq_length 512 \
  --output_dir $OUTPUT_DIR \
  --null_score_diff_threshold 0

# step-3
python scoring.py \
  --asqa ${ASQA_PATH} \
  --predictions ${PREDICTIONS_PATH} \
  --roberta_output ${OUTPUT_DIR}/eval_predictions.json \
  --split dev \
  --out_dir $OUTPUT_DIR







