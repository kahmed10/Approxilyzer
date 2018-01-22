#/!bin/bash

if [ $# -ne 6 ]; then
    echo "Usage: ./run_injection.sh [app_name] [fi_args] [app_ckpt_num] [app_output (in m5out)] [disk_image (in dist/m5/system/disks)] [id]"
    exit 1
fi

app_name=$1
fi_args=$2
ckpt=$3
app_output=$4
disk_image=$5
id=$6

out_id=$(( $6 % 208)) # 208 is the number of cores

GEM5_DIR="/shared/workspace/kahmed10/Approxilyzer/gem5"
DISK_DIR="/shared/workspace/kahmed10/Approxilyzer/dist/m5/system/disks"
OUT_DIR=$GEM5_DIR"/outputs"
out_file=$OUT_DIR/$app_name-${out_id}.output

#cd $GEM5_DIR

mkdir -p m5out_$id
ln -s $GEM5_DIR/m5out/cpt.* m5out_$id
ln -s $GEM5_DIR/m5out/$app_output m5out_$id

cleanup () {
    rm -f temp_${id}.txt
    rm -rf m5out_$id
}
touch $out_file


$GEM5_DIR/build/X86/gem5.fast --outdir=m5out_$id \
    $GEM5_DIR/configs/example/fs_fi.py --fi=${fi_args} \
    --disk-image=$DISK_DIR/$disk_image -r $ckpt &> temp_${id}.txt

if grep -q "Timeout" temp_${id}.txt; then 
    echo ${fi_args}"::Detected:Timeout" >> $out_file
    cleanup
    exit 0
fi

if [ -f "m5out_$id/output.txt" ]; then
    if cmp -s m5out_$id/$app_output m5out_$id/output.txt; then
        echo ${fi_args}"::Masked" >> $out_file

    else
        echo ${fi_args}"::SDC" >> $out_file

    fi
else
# debug code
#    if [ ! -f "m5out_$id/system.pc.com_1.terminal" ]; then
#        echo "Where is this?" >> $out_file
#        exit 0
#    fi
    if grep -q "segfault" m5out_$id/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:segfault" >> $out_file
    elif grep -q "error" m5out_$id/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:error" >> $out_file
    else
        echo ${fi_args}"::Detected:missing_file" >> $out_file

    fi
fi

cleanup
