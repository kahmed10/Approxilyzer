#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print("Usage: python append_ec.py [app_ec_tick_list] [app_inj_results]")
    exit()

tick_list = open(sys.argv[1]).read().splitlines()
app_inj_list = open(sys.argv[2]).read().splitlines()


tick_map = {line.split(',')[1]:line.split(',')[0] for line in tick_list}
tick_pc_map = {line.split(',')[1]:line.split(',')[2] for line in tick_list}

for line in app_inj_list:
    tick = line.split(',')[0]

    print("%s,%s,%s" % (tick_map[tick],tick_pc_map[tick],line))