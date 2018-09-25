#!/usr/bin/python

import sys 

# this script outputs the injection results only related to the original
# injection list
if len(sys.argv) != 3:
    print 'Usage: python clean_inj.py [outcomes_file] [orig_file]'
    exit()


outcomes_map = {i.split('::')[0]:i.split('::')[1] for i in open(sys.argv[1]).read().splitlines()}

orig_set = set(open(sys.argv[2]).read().splitlines())

for inj in outcomes_map:
    if inj in orig_set:
        print '%s::%s' % (inj, outcomes_map[inj])

