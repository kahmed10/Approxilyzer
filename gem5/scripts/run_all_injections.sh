#!/bin/bash

# INCOMPLETE

if [ $# -ne 4 ]; then
    echo "Usage: ./run_all_injections.sh [app_ckpt] [run_inj_file] [golden_app_output_file] [full_output]"
    exit
fi

app_num=$1
run_inj_file_list=$2
