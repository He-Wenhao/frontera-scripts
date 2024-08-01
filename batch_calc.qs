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

    
# SBATCH --mail-user='20010509@qq.com' 
# SBATCH --mail-type=END,FAIL,TIME_LIMIT_90


n_proc=30
core_per_task=10
slot_free=()
pids=()

method_folder=$1

# define environment settings orca and openmpi
env_settings=$(cat << 'EOF'
vpkg_require openmpi/4.1.5
export OMPI_MCA_btl=^openib
export ORCA=/lustre/xg-che240127/sw/packages/orca_6_0_0/orca
EOF
)



for ((i=0; i<$n_proc; i++)); do
    slot_free[$i]=1
done

echo "start:"$PATH

tol_start=$SECONDS
#export OMPI_MCA_btl=^openib
#export PMIX_MCA_psec=^munge
#source ~/.bash_profile



# Define a function to run and check mpi
run_orca=$(cat <<'EOF'


sub_start=$SECONDS
if grep -q "TOTAL RUN TIME:" log; then
    echo 'skip'
    :
else
    rm my_hostfile
    for i in $(seq 1 $1)
    do
        echo $3 >> my_hostfile
    done
    ssh -o StrictHostKeyChecking=no $3 "cd $4; source env_settings.sh; rm /tmp/run.gbw /tmp/*.tmp* /tmp/run.inp /tmp/run.ges; cp run.inp /tmp/run.inp; \$ORCA /tmp/run.inp > /tmp/log '-machinefile my_hostfile -v'; cp /tmp/log log; cp /tmp/run.densities run.densities;cp /tmp/run.properties run.properties; echo 'disk storage'\$( du -sh /tmp 2>/dev/null)"
fi

sub_duration=$(( SECONDS - sub_start ))
echo $(pwd)' run time: '$sub_duration


EOF
)


wait_flag=0
for i in {0..999}
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
    cd $i
    cd $method_folder
    echo $(pwd)
    echo "$run_orca" > run_orca.sh
    echo "$env_settings" > env_settings.sh
    #ibrun -n 1 -o $slot_id task_affinity bash run_orca.sh &
    # get host name
    host_name=$(scontrol show hostname $SLURM_NODELIST | sed -n $(expr $slot_id + 1)'p')
    #echo 'ssh '$host_name
    #ssh $host_name
    #echo $(pwd)
    #copy input file to /tmp
    #cp run.inp /tmp/run.inp
    #generate machine
    #for i in {1..$core_per_task}
    #do
    #    echo $host_name >> my_hostfile
    #done
    current_dir=$(pwd)
    echo $pwd' slot id:'$slot_id
    bash run_orca.sh  $core_per_task $((slot_id * core_per_task)) $host_name $current_dir &    # in ibrun style
    pids[$slot_id]=$!
    slot_free[$slot_id]=0
    #bash run_orca.sh &
    # Echo the result
    echo "Number of background jobs: $(jobs -l | wc -l)"
    if [ "$(jobs -l | wc -l)" -ne 1 ]; then
        sleep 1
    fi
    echo 'end of loop0:'$(pwd)
    cd ..
    cd ..
    echo 'end of loop:'$(pwd)
if [ $wait_flag -eq $n_proc ]; then
    break
fi
done

wait
echo 'all done'
