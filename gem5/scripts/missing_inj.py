#!/usr/bin/python

import sys 

# this script finds the missing injections that were missed due to errors
# in veena (out of space for example)
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print "Usage: python missing_inj.py [outcomes_file] [orig_file] (raw_flag)"
    exit()

raw_flag = False
outcomes_map = {}

if len(sys.argv) == 4:
    raw_flag = True
if raw_flag:
    outcomes_map = {i.split("::")[0] for i in open(sys.argv[1]).read().splitlines()}
else:
    outcomes_map = {item for item in open(sys.argv[1]).read().splitlines()}
orig_map = {item for item in open(sys.argv[2]).read().splitlines()}

for inj in orig_map:
    if inj not in outcomes_map:
        print inj 

