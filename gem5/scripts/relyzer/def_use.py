#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print("Usage: python def_use.py [parsed_dis_file]")
    exit()

dis_file = sys.argv[1]

# read and organize disassembly info (1st line is just header)
dis_info = [i.split() for i in open(dis_file).read().splitlines()[1:]]

pc_list = [item[0] for item in dis_info]
pc_map = { item[0]:None for item in dis_info }

reg_map = {}

for item in dis_info:
    pc = item[0]
    is_ctrl_op = item[2]
    src_reg = item[3]
    dest_reg = item[4]
    if is_ctrl_op == "True":  # reset map once leaving basic block
        reg_map = {}
    else:
        if dest_reg != "None":
            reg_map[dest_reg]=pc
        if src_reg in reg_map:
            pc_map[reg_map[src_reg]] = pc  # record pc of first use
            reg_map.pop(src_reg, None) 
for pc in pc_list:
    def_use_pair = pc
    if pc_map[pc] is not None:
        def_use_pair += " %s" % pc_map[pc]
    print(def_use_pair)
