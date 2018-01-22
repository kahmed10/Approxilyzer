#!/usr/bin/python

# gets register info and outputs final injection list

import sys
import random

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python inj_create.py [input_file] (num_samples)")
    exit()

sampling = False
num_samples=0
if len(sys.argv) == 3:
    sampling = True
    num_samples = sys.argv[2]


in_file=sys.argv[1]
in_list = open(in_file).read().splitlines()

int_reg_info_64 = [ "rax", "rbx", "rcx", "rdx", "rbp", "rsi", "rdi",
                "rsp", "r8", "r9", "r10", "r11", "r12", "r13",
                "r14", "r15" ]

int_reg_info_32 = [ "eax", "ebx", "ecx", "edx", "ebp", "esi", "edi",
                "esp" ]
int_reg_info_16 = [ "ax,", "bx", "cx", "dx", "bp", "si", "di", "sp" ]

int_reg_info_8 = [ "ah", "bh", "ch", "dh", "al", "bl", "cl", "dl" ] 

float_reg_info_128 = [ "xmm0", "xmm1", "xmm2", "xmm3", "xmm4" , "xxm5",
                       "xmm6", "xmm7", "xmm8", "xmm9", "xmm10", "xmm11",
                       "xmm12", "xmm13", "xmm14", "xmm15" ]

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


if not sampling:
    for line in in_list:
        temp = line.split(',')
        tick = temp[0]
        reg = temp[1]
        upper_lower_length = 4 # used to get MSBs and LSBs
        for i in range(upper_lower_length):
            if reg in reg_bits_map:
                print("%s,%s,%d,%d" % (tick,reg,reg_bits_map[reg]-i-1,
                    reg_int_float_map[reg]))
                print("%s,%s,%d,%d" % (tick,reg,i,
                    reg_int_float_map[reg]))
            else:
                print("%s not in list!" % reg)
else:
    random.shuffle(in_list)
    for i in range(int(num_samples)):
        temp = in_list[i].split(',')
        tick = temp[0]
        reg = temp[1]
        upper_lower_length = 4 # used to get MSBs and LSBs
        for i in range(upper_lower_length):
            if reg in reg_bits_map:
                print("%s,%s,%d,%d" % (tick,reg,reg_bits_map[reg]-i-1,
                    reg_int_float_map[reg]))
                print("%s,%s,%d,%d" % (tick,reg,i,
                    reg_int_float_map[reg]))
            else:
                print("%s not in list!" % reg)