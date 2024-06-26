function read_one(){
    cp /scratch1/08491/th1543/script/read.py .
    python3 read.py > log_read 2>&1
    cp *.json /scratch1/08491/th1543/rad_res
}


folder_list=$(ls -d */)
for fo in $folder_list; do
    cd $fo
    rad_folder_list=$(ls -d */)
    for rad_fo in $rad_folder_list; do
        cd $rad_fo
        pwd
        #sbatch -J t$(basename $(pwd)) recur_pvtz_continue.sh
        #sbatch -J d$(basename $(pwd)) submit_pvdz_continue.sh
        read_one &
        #cp /work2/09730/whe1/frontera/li-group/generate-data/more_rad/backup/script/submit_pvdz_continue.sh .
        cd ..
    done
    cd ..
    wait
done
