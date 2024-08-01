#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --tasks-per-node=10
#SBATCH --cpus-per-task=1
# SBATCH --mem-per-cpu=8G
# SBATCH --tmp=30G
# SBATCH --job-name=openmpi_job
#SBATCH --partition=standard
#SBATCH --time=0-02:00:00
# SBATCH --time-min=0-01:00:00
# SBATCH --output=%x-%j.out
# SBATCH --error=%x-%j.out
source ~/.bashrc
python3 generate_QM9_orca6.py
