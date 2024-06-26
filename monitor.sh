#nohup bash monitor.sh > nohup.log 2>&1 &
rm log- control.txt

while ! grep -q "done" log-$job_id; do
    # Place the commands you want to execute repeatedly here
    
    # Example: Echo a message
    echo 'self submited'
    output=$(sbatch operate_all.sh)
    echo $output
    job_id=$(echo $output | grep -oP "Submitted batch job \K[0-9]+")
    for i in {1..30}; do
        echo "Sleep Iteration $i; PID:$$; parent PID:$PPID; submitted job_id:$job_id"
        sleep 10
        if grep -q 'stop' control.txt; then
            break
        fi
    done   
    if grep -q 'stop' control.txt; then
        echo 'control.txt stop'
        break
    fi
done
