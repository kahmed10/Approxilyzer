#!/usr/bin/python

# This script computes the address bounds given the memory profile.

import os
import sys

if len(sys.argv) != 2:
    print('Usage: python bounding_address.py [app_name]')
    exit()

app_name = sys.argv[1]

approx_dir = os.environ.get('APPROXGEM5')

apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
if not os.path.exists(apps_dir):
    os.makedirs(approx_dir)

mem_file = apps_dir + '/' + app_name + '_mem_dump_parsed.txt'
mem_list = open(mem_file).read().splitlines()

min_addr = None
max_addr = None

for line in mem_list:
    temp = line.split()
    addr = int(temp[-1],16)
    if min_addr is None:
        min_addr = addr
        max_addr = addr
    if addr < min_addr:
        min_addr = addr
    if addr > max_addr:
        max_addr = addr

print('Min addr: 0x%x' % min_addr)
print('Max addr: 0x%x' % max_addr)

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
print('min bits not touched: %d' % min_count)
print('max bits not touched: %d' % max_count)

output_file = apps_dir + '/' + app_name + '_mem_bounds.txt'
output = open(output_file, 'w')
output.write('lower_limit upper_limit\n')
output.write('%s %s\n' % (lower_limit,upper_limit))
output.close()

