#python run_llama.py \
#    --ckpt_dir /usr/xtmp/qz124/misinfo_vax_ss23/llama/llama-2-7b/ \
#    --tokenizer_path --tokenizer_path /usr/xtmp/qz124/misinfo_vax_ss23/llama/tokenizer.model \
#    --max_seq_len 1024 --max_batch_size 4

export TRANSFORMERS_CACHE='/usr/xtmp/yh386/.cache/transformers'
export CUDA_VISIBLE_DEVICES='6'

python run.py --model "meta-llama/Llama-2-13b-chat-hf" \
       --dataset_name "eli5"
