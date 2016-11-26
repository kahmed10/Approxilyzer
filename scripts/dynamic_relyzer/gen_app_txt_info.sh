#!/bin/bash

# Generates the file "app_txt_info.py" for an application. 
# App_txt_info is used to pass parameters to Relyzer while running. 

script_content()
{
    T='    '
    
    if [ $# -ne 1 ]
    then
        echo "Wrong number of paramters passed into function script_content()"
        exit 1
    fi
    echo "# THE SKELETON OF THIS SCRIPT IS AUTOGENERATED."
    echo "# YOU HAVE TO FILL IN THE APPROPRIATE VALUES FOR EACH ARRAY"
    echo
    echo "# THE VALUES FOR TEXT_START AND TEXT_END ARE USUALLY EXTRACTED FROM THE DISASSEMBLY"
    echo "# THE VALUES FOR ACTUAL_APP_START AND END CAN BE THE SAME AS THE TEXT_START AND TEXT_END, RESPECTIVELY"
    echo "# YOU CAN REDUCE SIMULATION TIMES BY SPECIFYING AN ACTUAL START AND END BETWEEN THE EXTREMES"
    echo "# ACTUAL_APP_LENGTH IS THE DECIMAL VALUE OF INSTRUCTIONS EXECUTED BETWEEN THE ACTUAL START AND FINISH"
    echo "# ACTUAL_APP_LENGTH IS AUTOGENERATED IN A LATER STEP."
    echo "# IT CAN BE OBTAINED FROM THE *_app_length.txt FILE THAT IS GENERATED"
    echo
    echo
    echo "OPT_LEVEL=\"\""
    echo "text_start = {}"
    echo "text_end = {}"
    echo "actual_app_start= {}"
    echo "actual_app_end = {}"
    echo "actual_app_length = {}"
    echo
    echo "def init_txt_info():"
    echo
    echo -e "${T}if OPT_LEVEL == \"fully_optimized\" :"
    echo -e "${T}${T}text_start['${1}'] = 0xdeadbeef\t#FILL HERE"
    echo -e "${T}${T}text_end['${1}'] = 0xdeadbeef\t#FILL HERE"
    echo -e "${T}${T}actual_app_start['${1}'] = 0xdeadbeef\t#FILL HERE"
    echo -e "${T}${T}actual_app_end['${1}'] = 0xdeadbeef\t#FILL HERE"
    echo -e "${T}${T}actual_app_length['${1}'] = 00000000000000000000\t#WILL BE UPDATED AUTOMATICALLY"
#    echo -e "\t\ttext_start[\'${1}\'] = ${2}"
#    echo -e "\t\ttext_end[\'${1}\'] = ${3}"
#    echo -e "\t\tactual_app_start[\'${1}\'] = ${2}"
#    echo -e "\t\tactual_app_end[\'${1}\'] = ${3}"
#    echo -e "\t\tactual_app_length[\'${1}\'] = ${4}"
    echo -e "${T}else:"
    echo -e "${T}${T}print \"OPT_LEVEL NEEDS UPDATING\""
}

set -e

if [ $# -ne 1 ]; then
    echo "Usage: ./gen_app_txt_info.sh [app_name]"
    echo "Sample use: ./gen_simics_files_with_cmd_line.sh blackscholes_simlarge"
    echo
    echo "Warning: You should still look into the script to insure correct paths"
    exit 1
fi


### DIR STRUCTURE ###
DIR_0=$RELYZER_SHARED/workloads/apps/

if [[ ! -d $DIR_0/${1} ]]; then
    echo "No directory created for ${1} in workspace/app"
    exit 1
fi

DIR=${DIR_0}/${1}       # directory where all these scripts are made

#if [[ ! -d $DIR/analysis_output ]]; then
#    echo "No analysis files for ${1}"
#    exit 1
#fi

# IF APP TEXT INFO ALREADY EXISTS, DO NOT OVERRIDE IT! JUST QUIT!
if [[ ! -e $DIR/app_txt_info.py ]]; then
#    exit 0
#else
    #####################
    # get app start pc

    # get app end pc

    # get app length pc

    # call the script with the appropriate parameters
    script_content $1 > $DIR/app_txt_info.py

    echo
    echo "Please fill out the generated file at $DIR/app_txt_info.py with your desired values then rerun this script."
    echo
    exit 1
fi

if [[ -e $DIR/app_txt_info.py ]]; then
    value=$(grep "0xdeadbeef" "${DIR}/app_txt_info.py" | wc -l)
    if [ $value -eq 0 ]; then
        echo "app_txt_info.py previously edited"
    else
        echo
        echo "Please fill out the generated file at $DIR/app_txt_info.py with your desired values then rerun this script."
        echo
        exit 1
    fi
fi

