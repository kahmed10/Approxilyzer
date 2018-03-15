#!/bin/bash

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Usage: ./gen_exec_trace.sh [isa] [app] (disk_image_name)"
    exit 1
fi

isa=$1
app=$2
gem5_isa=$isa

GEM5_DIR=$APPROXGEM5/gem5
CKPT_DIR=$APPROXGEM5/workloads/$isa/checkpoint/$app
IMG_DIR=$APPROXGEM5/dist/m5/system/disks/

if [ "$isa" == "x86" ]; then
    gem5_isa="X86"
fi

if [ $# -eq 3 ]; then
    disk_image=$IMG_DIR/$3
    $GEM5_DIR/build/$gem5_isa/gem5.opt -d $CKPT_DIR \
    --debug-flags=ExecEnable,ExecUser,ExecEffAddr,ExecTicks,ExecMacro \
    --debug-file=${app}_dump.gz $GEM5_DIR/configs/example/fs.py \
    --disk-image=$disk_image -r 1
else
$GEM5_DIR/build/$gem5_isa/gem5.opt -d $CKPT_DIR \
--debug-flags=ExecEnable,ExecUser,ExecEffAddr,ExecTicks,ExecMacro \
--debug-file=${app}_dump.gz $GEM5_DIR/configs/example/fs.py -r 1
fi
