#/!bin/bash

if [ $# -ne 5 ]; then
    echo $#
    echo "Usage: ./run_injection_sparc.sh [app_name] [fi_args] [app_ckpt_num] [golden_app_output] [id]"
    exit 1
fi

app_name=$1
fi_args=$2
ckpt=$3
app_output=$4
id=$5

out_id=$(( $id % 208)) # 208 is the number of cores

CHKPT_DIR=$APPROXGEM5/workloads/sparc/checkpoint
GEM5_DIR=$APPROXGEM5/gem5
SCRIPTS_DIR=$GEM5_DIR/scripts/injections
DISK_DIR=$APPROXGEM5/dist/m5/system/disks
TMP_DIR=/scratch/kahmed10/m5out_$id
OUT_DIR=$GEM5_DIR/outputs/sparc
out_file=$OUT_DIR/$app_name-${out_id}.output

if [ -d $TMP_DIR ]; then
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


$GEM5_DIR/build/SPARC/gem5.fast --outdir=$TMP_DIR \
    $GEM5_DIR/configs/example/fs_fi.py --fi=${fi_args} \
     -r $ckpt &> $TMP_DIR/temp_${id}.txt

if grep -q "Timeout" $TMP_DIR/temp_${id}.txt; then 
    echo ${fi_args}"::Detected:Timeout" >> $out_file
    cleanup
    exit 0
fi

if grep -i -q "fault" $TMP_DIR/system.t1000.pterm; then
    echo ${fi_args}"::Detected:segfault" >> $out_file
    cleanup
    exit 0
elif grep -i -q "exception" $TMP_DIR/system.t1000.pterm; then
    echo ${fi_args}"::Detected:exception" >> $out_file
    cleanup
    exit 0
elif [ "$app_name" != "swaptions" ]; then
    if grep -i -q "error" $TMP_DIR/system.t1000.pterm; then
        echo ${fi_args}"::Detected:error" >> $out_file
        cleanup
        exit 0
    fi
elif grep -q "error" $TMP_DIR/system.t1000.pterm; then
    echo ${fi_args}"::Detected:error" >> $out_file
    cleanup
    exit 0
fi

app_faulty_output="output.txt"
if [ "$app_name" == "sobel" ]; then
    app_faulty_output="output.pgm"
fi
python $SCRIPTS_DIR/quick_parse.py $TMP_DIR/system.t1000.pterm > $TMP_DIR/$app_faulty_output
if [ ! -s "$TMP_DIR/$app_faulty_output" ]; then
    rm -f $TMP_DIR/$app_faulty_output
fi

if [ -f "$TMP_DIR/$app_faulty_output" ]; then
    if cmp -s $TMP_DIR/$app_output $TMP_DIR/$app_faulty_output; then
        echo ${fi_args}"::Masked" >> $out_file

    else
        result=`perl $SCRIPTS_DIR/app_level_analysis.pl $app_name $TMP_DIR/$app_faulty_output $id`
        echo ${fi_args}"::$result" >> $out_file
    fi
else
    echo ${fi_args}"::Detected:missing_file" >> $out_file
fi



cleanup
