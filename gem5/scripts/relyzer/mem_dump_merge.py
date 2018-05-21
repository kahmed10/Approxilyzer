#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print('Usage: python mem_dump_merge.py [app] [isa]')
    exit()

app = sys.argv[1]
isa = sys.argv[2]

orig_dump = app + '_dump_parsed.txt'
micro_dump = app + '_dump_parsed_micro.txt'
mem_dump = app + '_mem_dump_parsed.txt'
merged_dump = app + '_clean_dump_parsed_merged.txt'

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
    mem_map[tick] = (r_w, addr)

output = open(merged_dump, 'w')
for line in orig_list:
    temp = line.split()
    inst_num = temp[0]
    if isa == 'x86':
        for tick in micro_tick_map[inst_num]:
            if tick in mem_map:
                r_w = mem_map[tick][0]
                addr = mem_map[tick][1]
                line += ' %s %s' % (r_w, addr)
        
    else:
        if tick in mem_map:
            r_w = mem_map[inst_num][0]
            addr = mem_map[inst_num][1]
            line += ' %s %s' % (r_w, addr)
    output.write(line + '\n')
output.close()

