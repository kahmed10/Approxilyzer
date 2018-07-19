#!/usr/bin/python

# this script parses the trace and gets only the cycle and PC
# for x86, the ticks for the microinsts are also recorded

import gzip
import os
import sys

if len(sys.argv) != 5:
    print('Usage: python parse.py [app_name] [main_start] [main_end] [isa]')
    exit()

app_name = sys.argv[1]

main_start = sys.argv[2]
main_end = sys.argv[3]

inst_db_file = app_name + '_parsed.txt'

inst_db_list = open(inst_db_file).read().splitlines()[1:]
app_pcs = set(['0x' + i.split()[0] for i in inst_db_list])

isa = sys.argv[4]

approx_dir = os.environ.get('APPROXGEM5')

in_file_base = approx_dir + '/workloads/' + isa + '/checkpoint/' + \
               app_name + '/' + app_name
in_file_dump = in_file_base + '_dump.gz'

start_recording = False
stop_recording = False

dis_list = gzip.open(in_file_dump).read().splitlines()

inst_num_list = []
inst_num_pc_map = {}
inst_num_map = {}

apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
if not os.path.exists(apps_dir):
    os.makedirs(approx_dir)
outfile = apps_dir + '/' + app_name + '_dump_parsed.txt'
output = open(outfile, 'w')
for line in dis_list:
    if 'system.cpu' in line:
        temp = line.split()
        inst_num = temp[0].rstrip(': ')
        pc = temp[2]
        if (pc == main_start):
            start_recording = True
        if (pc == main_end):
            stop_recording = True
        if start_recording:
            if stop_recording:
                break
            if pc in app_pcs:
                output.write('%s %s\n' % (inst_num, pc))
                inst_num_list.append(inst_num)
                inst_num_pc_map[inst_num] = pc
                inst_num_map[inst_num] = []
output.close()

if isa == 'x86':
    start_recording = False
    stop_recording = False
    in_file_dump_micro = in_file_base + '_dump_micro.gz'
    
    dis_list = gzip.open(in_file_dump_micro).read().splitlines()

    inst_num_idx = 0
    for line in dis_list:
        if 'system.cpu' in line:
            temp = line.split()
            tick = temp[0].rstrip(': ')
            temp_pc_info = temp[2].split('.')
            pc = temp_pc_info[0]
            pc_num = ''
            if len(temp_pc_info)>1:
                pc_num = temp_pc_info[1]
            if (pc == main_start):
                start_recording = True
            if (pc == main_end):
                stop_recording = True
            if start_recording:
                if stop_recording:
                    break
                if pc in app_pcs:
                    if pc == inst_num_pc_map[inst_num_list[inst_num_idx]]:
                        if pc_num == '0':  # reset on context switch
                            inst_num_map[inst_num_list[inst_num_idx]]=[]
                        inst_num_map[inst_num_list[inst_num_idx]].append(tick)
                    else:
                        inst_num_idx += 1
                        inst_num_map[inst_num_list[inst_num_idx]].append(tick)

    outfile = apps_dir + '/' + app_name + '_dump_parsed_micro.txt'
    output = open(outfile, 'w')
    for inst_num in inst_num_list:
        output.write('%s:%s\n' % (inst_num,','.join(inst_num_map[inst_num])))
        

    output.close()
