#!/bin/bash

# combines many steps of pre-processing into one (in progress)

if [ $# -ne 1 ]; then
    echo "Usage (currently x86 only): ./relyzer.sh [app_name]"
    exit 1
fi

app_name=$1

if [ ! -f ${app_name}_parsed.txt ]; then
    python inst_database.py $APPROXGEM5/gem5/m5out/${app_name}.dis ${app_name}_parsed.txt
fi

python control_equivalence.py ${app_name}

python store_equivalence.py ${app_name}

python def_use.py ${app_name}

python bounding_address.py ${app_name}

python pruning_database.py ${app_name}

python inj_create.py ${app_name} x86 > ${app_name}_inj_list.txt
