DATASET_NAME="asqa"
MODEL_NAME="Llama-2-7b-chat-hf"

CONFIDENCE_METHOD="self_eval_repetition"
#CONFIDENCE_METHOD="self_repetition_claim"

SAMPLE_NUM=5
RESULT_DIR="./results"
python analysis.py --result_dir $RESULT_DIR --dataset_name $DATASET_NAME --model_name $MODEL_NAME --confidence_method $CONFIDENCE_METHOD --sample_num $SAMPLE_NUM

