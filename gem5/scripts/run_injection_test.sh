#/!bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: ./run_injection.sh [fi_args] [app_ckpt_num] [app_output (in m5out)]"
    exit 1
fi

fi_args=$1
ckpt=$2
app_output=$3

GEM5_DIR="/home/khalique/gem5"


mkdir -p m5out
cp -r $GEM5_DIR/m5out/cpt.* m5out
cp $GEM5_DIR/m5out/$app_output m5out

cleanup () {
    rm -f temp.txt
    rm -rf m5out
}




$GEM5_DIR/build/X86/gem5.fast $GEM5_DIR/configs/example/fs_fi.py --fi=${fi_args} \
    --disk-image=/dist/m5/system/disks/x86root-parsec_2.img -r $ckpt &> temp.txt

if grep -q "Timeout" temp.txt; then 
    echo ${fi_args}"::Detected:Timeout"
    cleanup
    exit 0
fi

if [ -f "m5out/output.txt" ]; then
    if cmp -s m5out/$app_output m5out/output.txt; then
        echo ${fi_args}"::Masked"
    else
        echo ${fi_args}"::SDC"
    fi
else
    if grep -q "segfault" m5out/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:segfault"
    elif grep -q "error" m5out/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:error"
    else
        echo ${fi_args}"::Detected:missing_file"
    fi
fi

cleanup
