#!/usr/bin/python

# this script parses the trace and gets only the cycle and PC
import sys

if len(sys.argv) != 4:
    print("Usage: python parse.py [in_file] [main_start] [main_end]")
    exit()

main_start = sys.argv[2]
main_end = sys.argv[3]

start_recording = False
stop_recording = False

dis_list = open(sys.argv[1]).read().splitlines()


for line in dis_list:
    if "system.cpu" in line:
        temp = line.split()
        cycle = temp[0].rstrip(": ")
        pc = temp[2]
        if (pc == main_start):
            start_recording = True
        if (pc == main_end):
            stop_recording = True
        if start_recording:
            if stop_recording:
                break
            print("%s %s" % (cycle, pc))
