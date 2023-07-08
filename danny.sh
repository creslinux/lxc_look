#!/bin/bash
# 20230606 <danny@hallwood.co.uk>

# .ext to match on
array_m=( 'mp3' 'flac' )
array_v=( 'mov' 'avi' )
array_i=( 'jpg' 'png' )

# Key is the folder name, *,values will be moved to
declare -A array
array=( [music]=${array_m[@]} [video]=${array_v[@]} [images]=${array_i[@]} )

for key in ${!array[@]}; do
    mkdir -p ${key}
    for value in ${array[${key}]}; do
        mv ${value} "${key}/${value}"
    done
done

# rm logs
find . -name "*.log" -exec rm -f {} \;
echo "done"
