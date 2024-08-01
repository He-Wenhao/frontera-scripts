#!/bin/bash -l
#SBATCH --nodes=30
#SBATCH --tasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH --tmp=30G
#SBATCH --job-name=openmpi_job
#SBATCH --partition=standard
#SBATCH --time=2-00:00:00
# SBATCH --time-min=0-01:00:00
# SBATCH --output=%x-%j.out
# SBATCH --error=%x-%j.out

    
#SBATCH --mail-user='20010509@qq.com' 
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_90

function run_one_calc {
    if grep -q "$1 finished" run_all.log; then
        echo "skip $1"
    else
        bash batch_calc.qs $1
        echo "$1 finished; timer = $SECONDS seconds" >> run_all.log
    fi
}

SECONDS=0

run_one_calc bp86
run_one_calc EOM
run_one_calc polar
run_one_calc pvdz_CCSDt
run_one_calc pvdz_DLPNO_CCSDt
run_one_calc pvtz_DLPNO_CCSDt




