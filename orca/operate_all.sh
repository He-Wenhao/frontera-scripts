
#folder_list=$(ls -d */)
folder_list=$(ls -d */ | grep -v -E '^(C3H4|C4H6)/$')
#for fo in C4H6 C4H8 
for fo in $folder_list
do
cd $fo
echo $(pwd)
#cp /scratch1/08491/th1543/script/generate_rad.py .
#python3 generate_rad.py
#cp /scratch1/08491/th1543/script/parallel_pvdz.sh .
bash parallel_pvdz.sh > log 2>&1
cd ..
done