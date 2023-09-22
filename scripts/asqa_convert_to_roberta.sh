
PREDICTIONS_PATH=./predictions/t5_predictions.json
OUTPUT_DIR=./results/t5
cd datasets/asqa
python convert_to_roberta_format.py  \
  --asqa /usr/xtmp/yh386/datasets/asqa/ASQA.json \
  --predictions ${PREDICTIONS_PATH}  \
  --split dev \
  --output_path ${OUTPUT_DIR}

