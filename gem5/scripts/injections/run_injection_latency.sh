#/!bin/bash

# Run

if [ $# -lt 6 ] || [ $# -gt 7 ]; then
    echo "Usage: ./run_injection_latency.sh [fi_args] [app_ckpt_num] [golden_file] [app_name] [id] [disk_image] (timeout)"
    echo "The golden file must exist in the m5out directory located at [APPROX_PATH]/gem5/m5out"
    echo "Use the filename only, so ignore the absolute path."
    exit 1
fi

fi_args=$1
ckpt=$2
golden_file=$3
timeout=""
app_name=$4
id=$5
disk_image=$6

out_id=$(( $5 % 208)) # 208 is the number of cores

if [ $# -eq 7 ]; then
    timeout=$7
fi

GEM5_DIR="/shared/workspace/kahmed10/Approxilyzer/gem5" # TODO: make scalable
DISK_DIR="/shared/workspace/kahmed10/Approxilyzer/dist/m5/system/disks"
OUT_DIR=$GEM5_DIR"/outputs"
out_file=$OUT_DIR/${app_name}_latency-${out_id}.output

mkdir -p m5out_$id
ln -s $GEM5_DIR/m5out/cpt.* m5out_$id
ln -s $GEM5_DIR/m5out/$golden_file m5out_$id

cleanup () {
    rm -f temp_${id}.txt
    rm -rf m5out_$id
}


if [ $# -eq 6 ]; then 
    $GEM5_DIR/build/X86/gem5.opt \
        --debug-flags=ExecEnable,ExecUser,ExecTicks,ExecEffAddr,ExecMacro \
        --debug-file=dead.tar.gz \
        --outdir=m5out_$id \
        $GEM5_DIR/configs/example/fs_fi.py --fi=$fi_args \
        --golden-file=$GEM5_DIR/m5out/$golden_file \
        --disk-image=$DISK_DIR/${disk_image} \
        -r $ckpt &> temp_${id}.txt
else
    $GEM5_DIR/build/X86/gem5.opt \
        --debug-flags=ExecEnable,ExecUser,ExecTicks,ExecEffAddr,ExecMacro \
        --debug-file=dead.tar.gz \
        --outdir=m5out_$id \
        $GEM5_DIR/configs/example/fs_fi.py --fi=$fi_args \
        --timeout=$timeout \
        --golden-file=$GEM5_DIR/m5out/$golden_file \
        --disk-image=$DISK_DIR/${disk_image} \
        -r $ckpt &> temp_${id}.txt
fi
time_end=`tail -1 temp_${id}.txt | awk '{if ($NF=="diverged") print $4}'`
#echo $time_end
time_start=`echo $fi_args | cut -d, -f1`
#echo $time_start
diff=$(($time_end-$time_start))
echo "$fi_args::Detected:::$diff" >> $out_file

cleanup

