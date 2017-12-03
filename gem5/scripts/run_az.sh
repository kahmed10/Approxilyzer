#!/bin/bash

if [ $# -ne 6 ]; then
    echo "Usage: ./run_az.sh [app_name] [inj_file] [ckpt_num] [output_file_check] [job_name] [start_idx]"
    exit 1
fi

app_name=$1
inj_file=$2
ckpt_num=$3
output_file=$4
job_name=$5
start_idx=$6

az batch account login -g batchResourceGroup -n kahmed10

#azJobTest="bash -c \"/ext/gem5/scripts/run_injection.sh 237976747471500,rdx,60,0 2 lu_run_min.output\""

az batch job create --id $job_name --pool-id testPool

i=$start_idx
while read line; do
    az batch task create --job-id $job_name --task-id task${i} \
    --command-line "bash /ext/gem5/scripts/run_injection.sh $app_name $line $ckpt_num $output_file"
    (( i++ ))
done < $inj_file

az batch job set --job-id $job_name --on-all-tasks-complete terminateJob