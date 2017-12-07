#!/bin/bash

# Test experiment locally using input file

if [ $# -ne 5 ]; then
    echo "Usage: ./run_all_injections.sh [run_inj_file] [app_name] [app_ckpt_num] [golden_file_name] [output_file_name]"
    exit 1
fi

run_inj_file=$1
app_name=$2
ckpt=$3
golden_file=$4
output=$5

GEM5_DIR="/home/khalique/Approxilyzer/gem5" # TODO: make scalable


# line will have the following format: equiv_class_id,pc,tick,reg,bit,src_dest::outcome
while read line; do
    temp=(${line//::/ })
    fields=(${temp[0]//,/ })
    tick=${fields[2]}
    reg=${fields[3]}
    bit=${fields[4]}
    src_dest=${fields[5]}

    time_end=`./run_injection_latency.sh $tick,$reg,$bit,$src_dest $ckpt $golden_file | tr -d '\n'`
    diff=$(($time_end-$tick)) 
    echo $line:::$diff >> $output

done < $run_inj_file