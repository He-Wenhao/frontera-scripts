for i in {5..13}
do
    cd $i
    #tar -czvf "orcaData$i.tar.gz" "orcaData$i/"
    rclone copy "orcaData$i.tar.gz" gdrive:/research-data/QM9-c0m1/result --verbose --progress
    cd ..
done

