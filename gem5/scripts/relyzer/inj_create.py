#!/usr/bin/python

# gets register info and outputs final injection list

import sys
import random

if len(sys.argv) != 3:
    print('Usage: python inj_create.py [app] [isa]')
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]
pruning_db_file = app_name + '_pruning_database.txt'
mem_bounds_file = app_name + '_mem_bounds.txt'


pruning_db = [i.split() for i in open(
    pruning_db_file).read().splitlines()[1:]]
mem_bounds = map(int, open(
             mem_bounds_file).read().splitlines()[1].split())
mem_bound = max(mem_bounds)


int_reg_info_64 = [ 'rax', 'rbx', 'rcx', 'rdx', 'rbp', 'rsi', 'rdi',
                'rsp', 'rip', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13',
                'r14', 'r15' ]

int_reg_info_32 = [ 'eax', 'ebx', 'ecx', 'edx', 'ebp', 'esi', 'edi',
                'esp', 'eip' ]
int_reg_info_16 = [ 'ax', 'bx', 'cx', 'dx', 'bp', 'si', 'di', 'sp', 'ip' ]

int_reg_info_8 = [ 'ah', 'bh', 'ch', 'dh', 'al', 'bl', 'cl', 'dl' ] 

upper_regs = set([ 'ah', 'bh', 'ch', 'dh' ])

float_reg_info_128 = [ 'xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4' , 'xmm5',
                       'xmm6', 'xmm7', 'xmm8', 'xmm9', 'xmm10', 'xmm11',
                       'xmm12', 'xmm13', 'xmm14', 'xmm15' ]

float_reg_info_64 = [ 'fpr0', 'fpr1', 'fpr2', 'fpr3', 'fpr4',
        'fpr5', 'fpr6', 'fpr7' ]

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

def print_inj(isa, pilot, bit_pos, reg, reg_type, src_dest):
    print('%s,%s,%s,%s,%s,%s' % (isa, pilot, reg, bit_pos,
                reg_type, src_dest))

def create_inj(isa, pilot, reg, max_bits, mem_bound=64):
    '''
    used for source registers only (0 passed in to src_dest)
    '''
    reg_max_bits = reg_bits_map[reg]
    reg_type = reg_int_float_map[reg]
    max_iter_bits = min(reg_max_bits, max_bits, mem_bound)
    for bit in range(max_iter_bits):
        print_inj(isa, pilot, bit, reg, reg_type, 0)

def create_def_inj(isa, pilot, pc, def_pc, max_bits):
    temp = def_pc.split(':')
    reg = temp[0]
    reg_max_bits = reg_bits_map[reg]
    reg_type = reg_int_float_map[reg]
    bit_widths = temp[1:]

    # edge case where only bits [15:8] are checked (like %ah)
    if reg in upper_regs:
        if bit_widths[1] == pc:
            for bit in range(reg_max_bits):
                print_inj(isa, pilot, bit, reg, reg_type, 1)
    else:
        # go through the bit widths and only inject if there was no first use
        if bit_widths[0] == pc:
            for bit in range(8):
                print_inj(isa, pilot, bit, reg, reg_type, 1)
        if bit_widths[1] == pc:
            for bit in range(8,16):
                print_inj(isa, pilot, bit, reg, reg_type, 1)
        if bit_widths[2] == pc:
            for bit in range(16,32):
                print_inj(isa, pilot, bit, reg, reg_type, 1)
        if bit_widths[3] == pc:
            for bit in range(32,min(max_bits,64)):
                print_inj(isa, pilot, bit, reg, reg_type, 1)
                    

for item in pruning_db:
    pc = item[0]
    def_pc = item[1]
    do_inject = item[2]
    src_regs = item[3]
    mem_src_regs = item[4]
    dest_reg = item[5]
    is_mem = item[6]
    pilot = item[7]
    max_bits = item[8]
    if do_inject == 'True':
        if src_regs != 'None':
            src_regs = src_regs.split(',')
            for src_reg in src_regs:
                create_inj(isa, pilot, src_reg, max_bits)
                
        if mem_src_regs != 'None':
            mem_src_regs = mem_src_regs.split(',')
            for mem_src_reg in mem_src_regs:
                create_inj(isa, pilot, mem_src_reg, max_bits, mem_bound)
                    
        # check destination register (pruning info found in def_pc)
        if def_pc != 'None':
            create_def_inj(isa, pilot, pc, def_pc, max_bits)

