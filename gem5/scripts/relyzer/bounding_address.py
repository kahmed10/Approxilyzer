#!/usr/bin/python

import sys

if len(sys.argv) != 2:
    print("Usage: python bounding_address.py [app]")
    exit()

app_name = sys.argv[1]
mem_file = app_name + "_mem_dump_parsed.txt"
mem_list = open(mem_file).read().splitlines()

min_addr = None
max_addr = None

for line in mem_list:
    temp = line.split()
    addr = temp[-1]
    if min_addr is None:
        min_addr = addr
        max_addr = addr
    if addr < min_addr:
        min_addr = addr
    if addr > max_addr:
        max_addr = addr

print("Min addr: %s" % min_addr)
print("Max addr: %s" % max_addr)
min_addr = int(min_addr,16)
max_addr = int(max_addr,16)

min_count = 0
max_count = 0

min_mask = 1 << 63
max_mask = min_mask

for i in range(64):  # maximum number of bits affected
    if ((min_mask >> i) & min_addr) > 0:
        min_count = i
        break
for i in range(64):
    if ((max_mask >> i) & max_addr) > 0:
        max_count = i
        break
lower_limit = 64 - min_count
upper_limit = 64 - max_count
print("min bits not touched: %d" % min_count)
print("max bits not touched: %d" % max_count)

output_file = "%s_mem_bounds.txt" % app_name
output = open(output_file, "w")
output.write("lower_limit upper_limit\n")
output.write("%s %s\n" % (lower_limit,upper_limit))
output.close()

