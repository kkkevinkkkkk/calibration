RESULT_PATH="./results/run/asqa/Llama-2-13b-chat-hf_predictions_500.json"

echo "$RESULT_PATH"
if echo "$RESULT_PATH" | grep -q "asqa"; then
  echo "dataset is asqa"
  python eval.py --f "$RESULT_PATH" --qa --gpt4_five_pnt
elif echo "$RESULT_PATH" | grep -q "eli5"; then
  echo "dataset is eli5"
  python eval.py --f "$RESULT_PATH" --claims_nli --gpt4_five_pnt
elif echo "$RESULT_PATH" | grep -q "qampari"; then
  echo "dataset is qampari"
  if echo "$RESULT_PATH" | grep -q "chat"; then
    echo "model is llama2-chat"
    python eval.py --f "$RESULT_PATH" --cot
  else
    echo "model not chat version"
    python eval.py --f "$RESULT_PATH"
  fi
else
  echo "dataset is unknown"
fi


