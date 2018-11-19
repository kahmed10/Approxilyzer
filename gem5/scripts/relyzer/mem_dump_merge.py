#!/usr/bin/python

# This script merges the isntruction and memory traces
# in order to create a simplified trace.

import os
import sys

if len(sys.argv) != 3:
    print('Usage: python mem_dump_merge.py [app_name] [isa]')
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]

approx_dir = os.environ.get('APPROXGEM5')

apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
if not os.path.exists(apps_dir):
    os.makedirs(approx_dir)

orig_dump = apps_dir + '/' + app_name + '_dump_parsed.txt'
micro_dump = apps_dir + '/' + app_name + '_dump_parsed_micro.txt'
mem_dump = apps_dir + '/' + app_name + '_mem_dump_parsed.txt'
merged_dump = apps_dir + '/' + app_name + '_clean_dump_parsed_merged.txt'

orig_list = open(orig_dump).read().splitlines()
micro_tick_map = {}
if isa == 'x86':
    micro_tick_map = {i.split(':')[0]:i.split(':')[1].split(',') for i in \
                      open(micro_dump).read().splitlines()}
mem_list = open(mem_dump).read().splitlines()
mem_map = {}

for line in mem_list:
    temp = line.split()
    tick = temp[0]
    r_w = temp[1]
    addr = temp[2]
    size = temp[3]
    mem_map[tick] = (r_w, addr, size)

output = open(merged_dump, 'w')
for line in orig_list:
    temp = line.split()
    inst_num = temp[0]
    if isa == 'x86':
        new_inst_num = micro_tick_map[inst_num][0]
        temp[0] = new_inst_num
        line = ' '.join(temp)
        for tick in micro_tick_map[inst_num]:
            if tick in mem_map:
                r_w = mem_map[tick][0]
                addr = mem_map[tick][1]
                size = mem_map[tick][2]
                line += ' %s %s %s' % (r_w, addr, size)
        
    else:
        if tick in mem_map:
            r_w = mem_map[inst_num][0]
            addr = mem_map[inst_num][1]
            size = mem_map[inst_num][2]
            line += ' %s %s %s' % (r_w, addr, size)
    output.write(line + '\n')
output.close()

