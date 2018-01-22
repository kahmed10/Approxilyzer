#/!bin/bash

if [ $# -ne 4 ]; then
    echo "Usage: ./run_injection.sh [app_name] [fi_args] [app_ckpt_num] [app_output (in m5out)]"
    exit 1
fi

app_name=$1
fi_args=$2
ckpt=$3
app_output=$4

GEM5_DIR="/ext/gem5"
OUT_DIR=$GEM5_DIR"/output"
out_file=$OUT_DIR/$app_name.output

#cd $GEM5_DIR

mkdir -p m5out
cp -r $GEM5_DIR/m5out/cpt.* m5out
cp $GEM5_DIR/m5out/$app_output m5out

cleanup () {
    rm -f temp.txt
    rm -rf m5out
}
touch $out_file


$GEM5_DIR/build/X86/gem5.fast $GEM5_DIR/configs/example/fs_fi.py --fi=${fi_args} \
    --disk-image=/dist/m5/system/disks/x86root-parsec.img -r $ckpt &> temp.txt

if grep -q "Timeout" temp.txt; then 
    echo ${fi_args}"::Detected:Timeout" >> $out_file
    cleanup
    exit 0
fi

if [ -f "m5out/output.txt" ]; then
    if cmp -s m5out/$app_output m5out/output.txt; then
        echo ${fi_args}"::Masked" >> $out_file

    else
        echo ${fi_args}"::SDC" >> $out_file

    fi
else
    if grep -q "segfault" m5out/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:segfault" >> $out_file

    else
        echo ${fi_args}"::Detected:missing_file" >> $out_file

    fi
fi

cleanup
