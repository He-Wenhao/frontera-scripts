
folder_list=$(ls -d */)
#for fo in C4H6 C4H8 
for fo in $folder_list
do
cd $fo
#sbatch -J t$(basename $(pwd)) recur_pvtz_continue.sh
#sbatch -J d$(basename $(pwd)) submit_pvdz_continue.sh
#cp /work2/09730/whe1/frontera/li-group/generate-data/more_rad/backup/script/recur_pvtz_continue.sh .
#cp /work2/09730/whe1/frontera/li-group/generate-data/more_rad/backup/script/submit_pvdz_continue.sh .
cp /work2/09730/whe1/frontera/li-group/generate-data/more_rad/backup/script/submit_pvdz_continue.sh .
cd ..
done