#/!bin/bash

# Run

if [ $# -lt 3 ] || [ $# -gt 4 ]; then
    echo "Usage: ./run_injection_latency.sh [fi_args] [app_ckpt_num] [golden_file] (timeout)"
    exit 1
fi

fi_args=$1
ckpt=$2
golden_file=$3
timeout=""

if [ $# -eq 4 ]; then
    timeout=$4
fi

GEM5_DIR="/home/khalique/Approxilyzer/gem5" # TODO: make scalable


mkdir -p m5out
cp -r $GEM5_DIR/m5out/cpt.* m5out

cleanup () {
    rm -f temp.txt
    rm -rf m5out
}


if [ $# -eq 3 ]; then 
    $GEM5_DIR/build/X86/gem5.opt \
        --debug-flags=ExecEnable,ExecUser,ExecTicks,ExecEffAddr,ExecMacro \
        --debug-file=dead.tar.gz \
        $GEM5_DIR/configs/example/fs_fi.py --fi=$fi_args \
        --golden-file=$golden_file
        --disk-image=/dist/m5/system/disks/x86root-parsec.img \
        -r $ckpt &> temp.txt
else
    $GEM5_DIR/build/X86/gem5.opt \
        --debug-flags=ExecEnable,ExecUser,ExecTicks,ExecEffAddr,ExecMacro \
        --debug-file=dead.tar.gz \
        $GEM5_DIR/configs/example/fs_fi.py --fi=$fi_args \
        --timeout=$timeout
        --golden-file=$golden_file
        --disk-image=/dist/m5/system/disks/x86root-parsec.img \
        -r $ckpt &> temp.txt
fi

cleanup

