#!/usr/bin/python

# this script parses the trace and gets only the cycle and PC
import gzip
import os
import sys

if len(sys.argv) != 5:
    print("Usage: python parse_mem.py [app_name] [main_tick_start] [main_tick_end] [isa]")
    exit()

app_name = sys.argv[1]
tick_start = sys.argv[2]
tick_end = sys.argv[3]
isa = sys.argv[4]

approx_dir = os.environ.get('APPROXGEM5')

in_file_base = approx_dir + '/workloads/' + isa + '/checkpoint/' + \
               app_name + '/' + app_name
in_file = in_file_base + '_mem_dump.gz'

start_recording = False
stop_recording = False

if in_file.split('.')[-1]  == "gz":
    dump_mem_list = gzip.open(in_file).read().splitlines()
else:
    dump_mem_list = open(in_file).read().splitlines()


out_filename = app_name + '_mem_dump_parsed.txt'
outfile = open(out_filename, 'w')
for line in dump_mem_list:
    temp = line.split()
    if len(temp) > 0:
        tick = temp[0].rstrip(": ")
        read_or_write = temp[2]
        if (tick >= tick_start):
            start_recording = True
        if (tick >= tick_end):
            stop_recording = True
        if start_recording:
            if stop_recording:
                break
            if "Read" in read_or_write  or "Write" in read_or_write:
                address = temp[10]  # consistent with gem5 tracer
                outfile.write("%s %s %s\n" % (tick, read_or_write, address))
outfile.close()
