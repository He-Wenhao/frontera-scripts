#!/bin/bash
#SBATCH -o log-%j
#SBATCH -N 11
#SBATCH --ntasks-per-node 1
#SBATCH -A DMR21001
#SBATCH -p development
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)

#sbatch -J pt$(basename $(pwd)) parallel_pvtz_plus.sh
n_proc=11
core_per_task=1
slot_free=()
pids=()

method_folder=$1

for ((i=0; i<$n_proc; i++)); do
    slot_free[$i]=1
done

echo "start:"$PATH

tol_start=$SECONDS
export PATH=$PATH:/work2/09730/whe1/bin
export LD_LIBRARY_PATH=/work2/09730/whe1/lib
export OMPI_MCA_btl=^openib
#export PMIX_MCA_psec=^munge
#source ~/.bash_profile

wait_flag=0

for i in {3..13}
do
    stop_flag=1
    slot_id=0
    while [ $stop_flag -eq 1 ]; do
        # check if there is available slot
        for ((ip=0; ip<$n_proc; ip++)); do
            if [ ${slot_free[ip]} -eq 1 ]; then
                slot_id=$ip
                stop_flag=0
                break
            fi
        done
        if [ $stop_flag -eq 0 ]; then
            break 
        fi
        # check if any pid terminates
        for p in "${!pids[@]}"; do
            if ! kill -0 ${pids[p]} 2>/dev/null; then
                # Process is not running, set slot availability
                slot_free[$p]=1
            fi
        done
    done
    echo 'before cd:'$(pwd)
    echo $(pwd)
    host_name=$(scontrol show hostname $SLURM_NODELIST | sed -n $(expr $slot_id + 1)'p')
    current_dir=$(pwd)
    echo $pwd' slot id:'$slot_id
    ssh $host_name "  source ~/.bashrc; cd $current_dir; tar -cvzf log_batch$i.tar.gz $i > tar_batch$i.log" &
    pids[$slot_id]=$!
    slot_free[$slot_id]=0
    echo "Number of background jobs: $(jobs -l | wc -l)"
    if [ "$(jobs -l | wc -l)" -ne 1 ]; then
        sleep 1
    fi
    echo 'end of loop0:'$(pwd)
    echo 'end of loop:'$(pwd)
if [ $wait_flag -eq $n_proc ]; then
    break
fi
done

wait
echo 'all done'
