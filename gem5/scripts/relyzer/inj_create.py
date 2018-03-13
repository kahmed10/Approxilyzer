#!/usr/bin/python

# gets register info and outputs final injection list

import sys
import random

if len(sys.argv) != 3:
    print("Usage: python inj_create.py [app] [isa]")
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]
fault_info_file = app_name + "_fault_list.txt"
mem_bounds_file = app_name + "_mem_bounds.txt"


fault_info = [i.split() for i in open(
    fault_info_file).read().splitlines()[1:]]
mem_bound = min([i.split() for i in open(
    mem_bounds_file).read().splitlines()[1:]])


int_reg_info_64 = [ "rax", "rbx", "rcx", "rdx", "rbp", "rsi", "rdi",
                "rsp", "r8", "r9", "r10", "r11", "r12", "r13",
                "r14", "r15" ]

int_reg_info_32 = [ "eax", "ebx", "ecx", "edx", "ebp", "esi", "edi",
                "esp" ]
int_reg_info_16 = [ "ax", "bx", "cx", "dx", "bp", "si", "di", "sp" ]

int_reg_info_8 = [ "ah", "bh", "ch", "dh", "al", "bl", "cl", "dl" ] 

float_reg_info_128 = [ "xmm0", "xmm1", "xmm2", "xmm3", "xmm4" , "xmm5",
                       "xmm6", "xmm7", "xmm8", "xmm9", "xmm10", "xmm11",
                       "xmm12", "xmm13", "xmm14", "xmm15" ]
float_reg_info_64 = [ "fpr0", "fpr1", "fpr2", "fpr3", "fpr4",
        "fpr5", "fpr6", "fpr7" ]

# set corresponding register info into map data structures
reg_bits_map = {}
reg_int_float_map = {}

for i in int_reg_info_64:
    reg_bits_map[i] = 64
    reg_int_float_map[i] = 0

for i in int_reg_info_32:
    reg_bits_map[i] = 32
    reg_int_float_map[i] = 0

for i in int_reg_info_16:
    reg_bits_map[i] = 16
    reg_int_float_map[i] = 0

for i in int_reg_info_8:
    reg_bits_map[i] = 8
    reg_int_float_map[i] = 0

for i in float_reg_info_128:
    reg_bits_map[i] = 64 # TODO: need to account for SIMD in the future
    reg_int_float_map[i] = 1

for i in float_reg_info_64:
    reg_bits_map[i] = 64
    reg_int_float_map[i] = 1

def print_inj(isa, pilot, reg, reg_max_bits, reg_type, src_dest):
    for i in range(reg_max_bits):
        print("%s,%s,%s,%s,%s,%s" % (isa, pilot, reg, i,
                reg_type, src_dest))

for item in fault_info:
    def_pc = item[1]
    do_inject = item[2]
    src_regs = item[3]
    dest_regs = item[4]
    is_mem = item[5]
    pilot = item[6]
    if do_inject != "False":
        if src_regs != "None":  #TODO: multiple src registers
            reg_max_bits = reg_bits_map[src_regs]
            reg_type = reg_int_float_map[src_regs]
            if is_mem == "True":
                reg_max_bits = min(reg_max_bits,mem_bound)
            print_inj(isa, pilot, src_regs, reg_max_bits, 
                    reg_type, 0)
                    
        if dest_regs != "None" and def_pc == "None":
            reg_max_bits = reg_bits_map[dest_regs]
            reg_type = reg_int_float_map[dest_regs]
            if is_mem == "True":
                reg_max_bits = min(reg_max_bits,mem_bound)
            print_inj(isa, pilot, dest_regs, reg_max_bits, 
                    reg_type, 1)


