#!/bin/bash
#SBATCH -o log-%j
#SBATCH -N 20
#SBATCH --ntasks-per-node 10
#SBATCH -A DMR23002
#SBATCH -p development
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)

#sbatch -J pt$(basename $(pwd)) parallel_pvtz_plus.sh
n_proc=20
core_per_task=10
slot_free=()
pids=()
for ((i=0; i<$n_proc; i++)); do
    slot_free[$i]=1
done

echo $PATH

tol_start=$SECONDS
export PATH=$PATH:/work2/09730/whe1/bin
export LD_LIBRARY_PATH=/work2/09730/whe1/lib
export OMPI_MCA_btl=^openib
#export PMIX_MCA_psec=^munge

# Define a function to run and check mpi
run_orca=$(cat <<'EOF'
echo 'running run_orca.sh '$$
sub_start=$SECONDS
if grep -q "TOTAL RUN TIME:" log; then
    echo 'skip'
    :
else
    if ls *.tmp 1> /dev/null 2>&1 || ls run.gbw 1> /dev/null 2>&1; then
        rm -rf *.tmp* run.gbw
        echo 'delete *.tmp* run.gbw'
    fi
    # generate machinefile
    #/scratch1/09730/whe1/li-tmp/test/my_ibrun -n $1 -o $2 echo 'generate_machinefile'
    #/work2/09730/whe1/frontera/orca/orca/orca /tmp/run.inp > log '-v --report-bindings -machinefile my_hostfile'
    /work2/09730/whe1/frontera/orca/orca/orca /tmp/run.inp > log '-machinefile my_hostfile'
    #rm my_ibrun
    #rm my_hostfile
fi

sub_duration=$(( SECONDS - sub_start ))
echo $pwd'run time: '$sub_duration

# if some issue happened, break
if ! grep -q "TOTAL RUN TIME:" log; then
    rm -rf *.tmp* run.gbw
    echo 'stop' > ../../../control.txt
    exit 1
fi
EOF
)

my_host_l=$(hostname)
echo 'hostname: '$my_host_l 

wait_flag=0

rad_folder_list=$(ls -d */)
for i in {0..99}
do
    for rad_folder in $rad_folder_list
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
        cd $rad_folder
        cd pvtz
        cd $i
        echo $(pwd)
        echo "$run_orca" > run_orca.sh
        #ibrun -n 1 -o $slot_id task_affinity bash run_orca.sh &
        # get host name
        host_name=$(scontrol show hostname $SLURM_NODELIST | head -n $(expr $slot_id + 1))
        ssh $host_name
        #copy input file to /tmp
        cp run.inp /tmp/run.inp
        #generate machine
        for i in {1..$core_per_task}
        do
        echo $host_name >> my_hostfile
        done
        bash run_orca.sh  $core_per_task $((slot_id * core_per_task)) &    # in ibrun style
        rm my_hostfile
        rm /tmp/run.inp
        pids[$slot_id]=$!
        slot_free[$slot_id]=0
        #bash run_orca.sh &
        # Echo the result
        echo "Number of background jobs: $(jobs -l | wc -l)"
        cd ..
        cd ..
        cd ..
    done
    if [ $wait_flag -eq $n_proc ]; then
        break
    fi
done

wait
echo 'all done'