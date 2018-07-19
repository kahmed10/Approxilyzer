#!/usr/bin/python

# This script creates validation information

import os
import sys
import random

from equiv_class import equiv_class_database
from pruning_database import pc_info

if len(sys.argv) != 3:
    print("Usage: python inj_validation_create.py [app] [isa]")
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]


approx_dir = os.environ.get('APPROXGEM5')
apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
app_prefix = apps_dir + '/' + app_name

pruning_db_file = app_prefix + "_pruning_database.txt"
mem_bounds_file = app_prefix + "_mem_bounds.txt"
ctrl_equiv_file = app_prefix + "_control_equivalence.txt"
store_equiv_file = app_prefix + "_store_equivalence.txt"


pruning_db = [pc_info(None,None,None,in_string=i) for i in open(
        pruning_db_file).read().splitlines()[1:]]
mem_bounds = map(int,open(
    mem_bounds_file).read().splitlines()[1].split())
mem_bound = max(mem_bounds)

seed_val = random.seed(1)
conf_95 = 385

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


store_equiv_db = equiv_class_database(app_prefix + '_store_equivalence.txt',
        get_members=True)
ctrl_equiv_db = equiv_class_database(app_prefix + '_control_equivalence.txt',
        get_members=True)
store_ids = store_equiv_db.get_above_average_pops()
ctrl_ids = ctrl_equiv_db.get_above_average_pops()

random.shuffle(store_ids)
random.shuffle(ctrl_ids)

def print_inj(isa, pilot, reg, max_iters, reg_type, src_dest, stride):
    injs = []
    for i in range(0,max_iters,stride):
        injs.append("%s,%s,%s,%s,%s,%s" % (isa, pilot, reg, i,
                reg_type, src_dest))
    return injs

def create_inj(equiv_db, pilot, regs,
               max_bits, mem_bounds=64, stride=8):
    injs = []
    i = 0
    members = equiv_db.get_members(pilot)
    random.shuffle(members)
    max_members = min(len(members),conf_95)
    for i in range(max_members):
        member = members[i]
        if member != pilot:
            for reg in regs:
                reg_max_bits = reg_bits_map[reg]
                reg_type = reg_int_float_map[reg]
                max_iters = min(reg_max_bits, max_bits, mem_bounds)
                injs += print_inj(isa, member, reg, max_iters, reg_type,
                                   0, stride) 
    return injs
    
store_injs = []
ctrl_injs = []
max_injs = 200000

pruning_db_map = {item.pilot:item for item in pruning_db}

temp = []
for ctrl_id in ctrl_ids:
    if ctrl_id in pruning_db_map:
        temp.append(ctrl_id)
ctrl_ids = temp

max_store_equiv = min(len(store_ids),conf_95)
max_ctrl_equiv = min(len(ctrl_ids),conf_95)

def add_validation_injs(injs, equiv_db, equiv_ids, max_equiv):
    for i in range(max_equiv):
        pilot = equiv_ids[i]
        pc_info = pruning_db_map[pilot]
        regs = pc_info.src_regs
        mem_regs = pc_info.mem_src_regs
        max_bits = pc_info.max_bits
        if regs is not None:
            injs += create_inj(equiv_db, pilot, regs,
                        max_bits)
        if mem_regs is not None:
            injs += create_inj(equiv_db, pilot, mem_regs,
                        max_bits, mem_bounds=mem_bound)
        if len(injs) > max_injs:
            break

add_validation_injs(store_injs, store_equiv_db, store_ids, max_store_equiv)
add_validation_injs(ctrl_injs, ctrl_equiv_db, ctrl_ids, max_ctrl_equiv)

print(len(store_injs))
print(len(ctrl_injs))

outfilename = app_prefix + '_new_validation_inj.txt'
outfile = open(outfilename,'w')
for inj in store_injs:
    outfile.write('%s\n' % inj)
for inj in ctrl_injs:
    outfile.write('%s\n' % inj)
outfile.close()
