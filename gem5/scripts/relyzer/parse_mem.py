#!/usr/bin/python

# This script parses the memory trace and uses the ROI provided
# from the instruction trace to remove external memory accesses.

import gzip
import os
import sys

if len(sys.argv) != 3:
    print('Usage: python parse_mem.py [app_name] [isa]')
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]

approx_dir = os.environ.get('APPROXGEM5')

in_file_base = approx_dir + '/workloads/' + isa + '/checkpoint/' + \
               app_name + '/' + app_name
in_file = in_file_base + '_mem_dump.gz'

start_recording = False
stop_recording = False

#if in_file.split('.')[-1]  == 'gz':
#    dump_mem_list = gzip.open(in_file).read().splitlines()
#else:
#    dump_mem_list = open(in_file).read().splitlines()


apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name

micro_inst_tracefile = apps_dir + '/' + app_name + '_dump_parsed_micro.txt'

#Not platform independent. ToDo fix
stdin,stdout = os.popen2("head -1 " + micro_inst_tracefile)
stdin.close()
head = stdout.read().splitlines()
stdout.close()
if len(head) != 1:
	sys.exit("Error reading the first line of micro dump") # Should only read the first line of the file
tick_start = head[0].split(':')[1].split(',')[0]

stdin,stdout = os.popen2("tail -1 " + micro_inst_tracefile)
stdin.close()
tail = stdout.read().splitlines();
stdout.close()
if len(tail) != 1:
	sys.exit("Error reading the last line of micro dump") # Should only read the last line of the file
tick_end = tail[-1].split(':')[1].split(',')[-1]

assert tick_end > tick_start, "Cycle number at execution start should be smaller than cycle number at end"
#print tick_start, tick_end


out_filename = apps_dir + '/' + app_name + '_mem_dump_parsed.txt'
outfile = open(out_filename, 'w')

with gzip.open(in_file) as infile:
    for line in infile:
		line = line.strip()
		temp = line.split()
		if len(temp) > 0:
			tick = temp[0].rstrip(': ')
			read_or_write = temp[2]
			if (tick >= tick_start):
				start_recording = True
			if (tick >= tick_end):
				stop_recording = True
			if start_recording:
				if stop_recording:
					break
				if 'Read' in read_or_write  or 'Write' in read_or_write and 'cpu.data' in temp[4]:
					if len(temp) < 13:
						print 'Error parsing following line: ', temp
						exit()
					address = temp[10]  # consistent with gem5 tracer
					data = temp[12]  # consistent with gem5 tracer
					size = temp[7]  # consistent with gem5 tracer
					outfile.write('%s %s %s %s %s\n' % (tick, read_or_write, address, size, data))

outfile.close()



