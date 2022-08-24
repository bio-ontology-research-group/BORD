#!/bin/bash --login
#SBATCH --time 02:00:00
#SBATCH --gpus=1
#SBATCH --cpus-per-gpu=6
#SBATCH --mem=90G
###SBATCH --mem-per-gpu=90G
#SBATCH --constraint=v100
####gtx1080ti
####p100
####v100
#SBATCH --partition=batch
#SBATCH -e slurm.%N.%j.err # STDERR 


# activate the conda environment
conda activate /ibex/scratch/kafkass/NER/conda-environment-examples/env

# start the nvdashboard server in the background
NVDASHBOARD_PORT=8000
python -m jupyterlab_nvdashboard.server $NVDASHBOARD_PORT &
NVDASHBOARD_PID=$!

#python predict_NER_iob.py  >./prediction_results/NoAbbr_shared.predictions.medmentions.lex.txt
python predict_NER_iob.py $1 >./predictions.txt

# kill off the GPU monitoring processes
kill $NVDASHBOARD_PID
