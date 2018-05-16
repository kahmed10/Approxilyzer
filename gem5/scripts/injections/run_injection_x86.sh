#/!bin/bash

if [ $# -ne 6 ]; then
    echo "Usage: ./run_injection_x86.sh [app_name] [fi_args] [app_ckpt_num] [app_output (in m5out)] [disk_image (in dist/m5/system/disks)] [id]"
    exit 1
fi

app_name=$1
fi_args=$2
ckpt=$3
app_output=$4
disk_image=$5
id=$6

out_id=$(( $id % 208)) # 208 is the number of cores

CHKPT_DIR=$APPROXGEM5/workloads/x86/checkpoint
GEM5_DIR=$APPROXGEM5//gem5
SCRIPTS_DIR=$GEM5_DIR/scripts/injections
DISK_DIR=$APPROXGEM5/dist/m5/system/disks
TMP_DIR=/scratch/kahmed10/m5out_$id
OUT_DIR=$GEM5_DIR/outputs/x86
out_file=$OUT_DIR/$app_name-${out_id}.output

if [ -d $TMP_DIR ]; then  # as a sanity check for now
    rm -rf $TMP_DIR
fi

mkdir -p $TMP_DIR
ln -s $CHKPT_DIR/$app_name/cpt.* $TMP_DIR
ln -s $CHKPT_DIR/$app_name/$app_output $TMP_DIR

cleanup () {
    rm -f temp_${id}.txt
    rm -rf $TMP_DIR
}
touch $out_file

app_faulty_output="output.txt"
if [ "$app_name" == "sobel" ]; then
    app_faulty_output="output.pgm"
fi
$GEM5_DIR/build/X86/gem5.fast --outdir=$TMP_DIR \
    $GEM5_DIR/configs/example/fs_fi.py --fi=${fi_args} \
    --disk-image=$DISK_DIR/$disk_image -r $ckpt &> $TMP_DIR/temp_${id}.txt

if grep -q "Timeout" $TMP_DIR/temp_${id}.txt; then 
    echo ${fi_args}"::Detected:Timeout" >> $out_file
    cleanup
    exit 0
fi

if [ -f "$TMP_DIR/${app_faulty_output}" ]; then
    if grep -i -q "segfault" $TMP_DIR/${app_faulty_output}; then
        echo ${fi_args}"::Detected:segfault" >> $out_file
        cleanup
        exit 0
    fi
    if cmp -s $TMP_DIR/$app_output $TMP_DIR/${app_faulty_output}; then
        echo ${fi_args}"::Masked" >> $out_file

    else
        result=`perl $SCRIPTS_DIR/app_level_analysis.pl $app_name $TMP_DIR/${app_faulty_output} $id`
        echo ${fi_args}"::$result" >> $out_file

    fi
else
    if grep -q "segfault" $TMP_DIR/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:segfault" >> $out_file
    elif grep -q "error" $TMP_DIR/system.pc.com_1.terminal; then
        echo ${fi_args}"::Detected:error" >> $out_file
    else
        echo ${fi_args}"::Detected:missing_file" >> $out_file

    fi
fi

cleanup