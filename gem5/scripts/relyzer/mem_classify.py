#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print("Usage: python mem_classify.py [app]")
    exit()

app_name = sys.argv[1]
trace_file = app_name + "_clean_dump_parsed_merged.txt"
trace_list = [i.split() for i in open(trace_file).read(
        ).splitlines()]
pc_mem_set = set()

for item in trace_list:
    if len(item) > 2:
        pc = item[1][2:]
        pc_mem_set.add(pc)

output_file = "%s_mem_insts.txt" % app_name
output = open(output_file, "w")
for pc in pc_mem_set:
    output.write("%s\n" % pc)
output.close()
