#!/bin/bash
#SBATCH -o log-%j
#SBATCH -N 20
#SBATCH --ntasks-per-node 10
#SBATCH -A DMR23002
#SBATCH -p development
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)


bash batch_calc.sh bp86
echo 'bp86 finished'
bash batch_calc.sh EOM
echo 'bp86 EOM'