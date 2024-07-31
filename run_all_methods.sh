#!/bin/bash
#SBATCH -o log-%j
#SBATCH -N 64
#SBATCH --ntasks-per-node 10
#SBATCH -A DMR21001
#SBATCH -p normal
#SBATCH -t 48:00:00        # Run time (hh:mm:ss)

function run_one_calc {
    if grep -q "$1 finished" run_all.log; then
        echo "skip $1"
    else
        bash batch_calc.sh $1
        echo "$1 finished; timer = $SECONDS seconds" >> run_all.log
    fi
}

SECONDS=0

run_one_calc bp86
#run_one_calc EOM
#run_one_calc polar
run_one_calc pvdz_CCSDt
run_one_calc pvdz_DLPNO_CCSDt
run_one_calc pvtz_DLPNO_CCSDt

run_one_calc pvdz_DLPNO_CCSD
run_one_calc pvtz_DLPNO_CCSD



