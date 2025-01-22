#nohup bash auto_queue.sh > aq_nohup.log 2>&1 &
rm log- aq_control.txt

# Define the function
monitor_job_submission() {
    local submit_command="$1"
    while ! grep -q "done" log-$job_id; do
        # Example: Echo a message
        echo 'self submited'

        # Execute the submission command and capture the output
        output=$($submit_command)
        echo "$output"

        # Extract job ID from the output
        job_id=$(echo "$output" | grep -oP "Submitted batch job \K[0-9]+")

        if [[ -n "$job_id" ]]; then
            echo "submitted job_id:$job_id"
            break
        fi

        # Sleep loop
        for i in {1..30}; do
            echo "Sleep Iteration $i; PID:$$; parent PID:$PPID"
            sleep 10
            if grep -q 'stop' aq_control.txt; then
                break
            fi
        done

        # Check if 'stop' is present in aq_control.txt
        if grep -q 'stop' aq_control.txt; then
            echo 'control.txt stop'
            break
        fi
    done
}

# Example usage of the function
monitor_job_submission "sbatch batch_test.sh"
monitor_job_submission "sbatch batch_test.sh"
monitor_job_submission "sbatch batch_test.sh"
