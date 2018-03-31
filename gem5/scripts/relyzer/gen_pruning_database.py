#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print("Usage: python gen_pruning_database.py [app]")
    exit()

# object to collect static pc info in fault database
class pc_info:
    def __init__(self, pc, pilot=None, is_mem="False"):
        self.pc = pc
        self.def_pc = None
        self.do_inject = "True"
        self.src_regs = None
        self.dest_regs = None
        self.is_mem = is_mem
        self.pilot = pilot
    def __repr__(self):
        return "PC object:%s" % self.pc

def check_string(obj):
    string = "None"
    if obj is not None:
        string = obj
    return string

ignored_ops = {"clr,prefetch"}

app_name = sys.argv[1]
ctrl_equiv_file = app_name + "_control_equivalence.txt"
store_equiv_file = app_name + "_store_equivalence.txt"
def_use_file = app_name + "_def_use.txt"
mem_inst_file = app_name + "_mem_insts.txt"
parsed_dis_file = app_name + "_parsed.txt"

ctrl_equiv_info = [i.split(':') for i in open(
        ctrl_equiv_file).read().splitlines()[1:]]
store_equiv_info = [i.split(':') for i in open(
        store_equiv_file).read().splitlines()[1:]]
def_use_info = {i.split()[0]:i.split()[1] for i in open(
        def_use_file).read().splitlines()[1:]}
mem_inst_info = set([i for i in open(
        mem_inst_file).read().splitlines()])
pc_regs_info = {i.split()[0]:i.split()[1:] for i in open(
        parsed_dis_file).read().splitlines()[1:]}

pc_map = {}
# when converting pc_regs_info to a map, indices are reduced by 1
op_idx = 0
src_reg_idx = 2
dest_reg_idx = 3
for item in ctrl_equiv_info:
    pc = item[0]
    pilot = item[2]
    pc_obj = pc_info(pc,pilot)
    pc_obj.op = pc_regs_info[pc][op_idx]
    if pc in def_use_info:
        pc_obj.def_pc = def_use_info[pc]
        # check if there are source registers
        if pc_regs_info[pc][src_reg_idx] == "None":
            pc_obj.do_inject = "False"
    if pc in mem_inst_info:
        pc_obj.is_mem = "True"
    pc_obj.src_regs = pc_regs_info[pc][src_reg_idx]
    pc_obj.dest_regs = pc_regs_info[pc][dest_reg_idx]
    if pc not in pc_map:
        pc_map[pc] = []
    if pc_obj.src_regs != "None" or  pc_obj.dest_regs != "None" and \
            pc_obj.op not in ignored_ops:
        pc_map[pc].append(pc_obj)

for item in store_equiv_info:
    pc = item[0]
    pilot = item[2]
    pc_obj = pc_info(pc,pilot,"True")
    pc_obj.src_regs = pc_regs_info[pc][src_reg_idx]
    if pc not in pc_map:
        pc_map[pc] = []
    pc_map[pc].append(pc_obj)

pc_list = sorted(pc_map.keys())
output_file = app_name + "_pruning_database.txt"
output = open(output_file, "w")
output.write("pc def_pc do_inject src_regs dest_regs is_mem pilot\n")
for pc in pc_list:
    for pc_obj in pc_map[pc]:
        def_pc = check_string(pc_obj.def_pc)
        do_inject = check_string(pc_obj.do_inject)
        src_regs = check_string(pc_obj.src_regs)
        dest_regs = check_string(pc_obj.dest_regs)
        is_mem = check_string(pc_obj.is_mem)
        pilot = check_string(pc_obj.pilot)
        output.write("%s %s %s %s %s %s %s\n" % (pc, def_pc,
            do_inject, src_regs, dest_regs, is_mem, pilot))
output.close()
