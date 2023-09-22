
export TRANSFORMERS_CACHE='/usr/xtmp/yh386/.cache/transformers'
export CUDA_VISIBLE_DEVICES='7'

torchrun --nproc_per_node 1 run.py \
        --model "meta-llama/Llama-2-7b-chat-hf" \
        --dataset_name "eli5"
#torchrun --nproc_per_node 1 run_llama.py \
#    --ckpt_dir /usr/xtmp/qz124/misinfo_vax_ss23/llama/llama-2-7b/ \
#    --tokenizer_path /usr/xtmp/qz124/misinfo_vax_ss23/llama/tokenizer.model \
#    --max_seq_len 1024 --max_batch_size 4

