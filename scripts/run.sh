#!/bin/bash
#SBATCH --job-name=$1    # job name, "OMP_run"
#SBATCH --partition=nlplab  # partition (queue)
#SBATCH -t 0-5:00              # time limit: (D-HH:MM)
#SBATCH --mem=32000            # memory per node in MB
#SBATCH --nodes=1              # number of nodes
#SBATCH --ntasks-per-node=1   # number of cores
#SBATCH --gres=gpu:a6000:1     # numer of GPUs
#SBATCH --output=log/tmp.out     # file to collect standard output
#SBATCH --error=log/tmp.err      # file to collect standard errors


CONFIG_NAME='v0.0.0'

if [ $# -eq 1 ]; then
    CONFIG_NAME=$1
fi
CONFIG_PATH="configures/$CONFIG_NAME.yml"

echo $CONFIG_PATH
python run.py --config_path "$CONFIG_PATH"