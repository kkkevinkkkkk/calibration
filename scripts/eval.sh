
export TRANSFORMERS_CACHE='/usr/xtmp/yh386/.cache/transformers'
export CUDA_VISIBLE_DEVICES='6'

#RESULT_PATH="./datasets/eli5/predictions/Llama-2-13b-chat-hf_predictions.json"
#python eval.py --f "$RESULT_PATH" --claims_nli --mauve

RESULT_PATH="/usr/xtmp/yh386/calibration/predictions/asqa/Llama-2-7b-hf_predictions.json"
python eval.py --f "$RESULT_PATH" --qa

