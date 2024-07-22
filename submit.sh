#!/bin/bash
#SBATCH -o log-%j
#SBATCH -N 1
#SBATCH --ntasks-per-node 50
#SBATCH -A DMR23002
#SBATCH -p development
#SBATCH -t 2:00:00        
source ~/.bashrc
/work2/09730/whe1/anaconda3/envs/ML_DFT/bin/python generate_QM9.py
