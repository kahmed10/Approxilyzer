#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print("Usage: python profile.py [dis_file] [dump_file]")
    exit()

dis_list = open(sys.argv[1]).read().splitlines()

dump_list = open(sys.argv[2]).read().splitlines()
pc_list = []
pc_map = {}

# for now, I am not using regex since I am focused on extracting PCs only
for line in dis_list:
    temp = line.split(':')
    if len(temp) != 0:
        if "<" not in temp[0]:
            pc = "0x%s" % temp[0].strip()
            pc_map[pc] = 0
            pc_list.append(pc)

for line in dump_list:
    temp = line.split()
    if temp[1] in pc_map:
        pc_map[temp[1]] += 1

for pc in pc_list:
    if pc_map[pc] > 0:
        print("%s:%d" % (pc,pc_map[pc]))

            
