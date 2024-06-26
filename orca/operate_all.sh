#!/bin/bash
#SBATCH -o log-%j
#SBATCH -N 20
#SBATCH --ntasks-per-node 10
#SBATCH -A DMR23002
#SBATCH -p development
#SBATCH -t 2:00:00        # Run time (hh:mm:ss)

# recursively run 
recurse_run(){
    if grep -q "all done" log; then
        echo 'skip'
        :
    else
        rm log
        bash parallel_pvtz.sh > log 2>&1
    fi
}

folder_list=$(ls -d */)
#folder_list=$(ls -d */ | grep -v -E '^(C3H4|C4H6)/$')
#for fo in C4H6 C4H8 
for fo in $folder_list
    do
    cd $fo
    echo $(pwd)
    #cp /scratch1/08491/th1543/script/generate_rad.py .
    #python3 generate_rad.py
    #cp /scratch1/08491/th1543/script/parallel_pvtz.sh .
    #rm log
    recurse_run
    cd ..
done
echo 'done'
