#!/usr/bin/python

import os
import sys

if len(sys.argv) != 3:
    print("Usage: python validation_stats.py [app] [isa]")
    exit()

app_name = sys.argv[1]
isa = sys.argv[2]
approx_dir = os.environ.get('APPROXGEM5')
apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
app_prefix = apps_dir + '/' + app_name
outcomes_dir = approx_dir + '/gem5/outputs/' + isa
outcomes_prefix = outcomes_dir + '/' + app_name

ctrl_equiv_file = app_prefix + '_final_control_equivalence.txt'
store_equiv_file = app_prefix + '_final_store_equivalence.txt'
dump_file = app_prefix + '_clean_dump_parsed_merged.txt'

valid_file = outcomes_prefix + '_validation.outcomes_raw'
orig_file = outcomes_prefix + '.outcomes_raw'

control_equiclass_map = {}
store_equiclass_map = {}

control_equiclass_info = [i.split(':') for i in open(
                          ctrl_equiv_file).read().splitlines()[1:]]
store_equiclass_info = [i.split(':') for i in open(
                        store_equiv_file).read().splitlines()[1:]]

cycle_pc_map = {i.split()[0]:i.split()[1][2:] for i in open(
                dump_file).read().splitlines()}

outcomes = open(valid_file).read().splitlines()
orig_outcomes = open(orig_file).read().splitlines()

pc_idx = 0
pilot_idx = 2
members_idx = 3

cycle_idx = 1
reg_idx = 2
bit_idx = 3
src_dest_idx = 5

def populate_equiclass_map(equiclass_map, equiclass_info):
    for line in equiclass_info:
        pc = line[pc_idx]
        if pc == '4012a3':
            a = 1
        pilot = line[pilot_idx]
        members = line[members_idx].lstrip().split()  # separated by spaces
        if pc not in equiclass_map:
            equiclass_map[pc] = {}
        equiclass_map[pc][pilot] = members

def find_equiv_id(pilot_map, cycle):
    equiv_id = ""
    for pilot in pilot_map:
        found_pilot = False
        for cycles in pilot_map[pilot]:
            if cycle == cycles:
                equiv_id = pilot
                found_pilot = True
                break
        if found_pilot:
            break
    return equiv_id


populate_equiclass_map(control_equiclass_map,control_equiclass_info)
populate_equiclass_map(store_equiclass_map,store_equiclass_info)

# sdc_idx = 0
# det_idx = 1
# masked_idx = 2
# percent_idx = 3

orig_outcomes_map = {}
for outcome in orig_outcomes:
    temp = outcome.split('::')
    temp1 = temp[0].split(',')
    pilot = temp1[1]
    pc = cycle_pc_map[pilot]
    reg = temp1[2]
    bit = temp1[3]
    src_dest = temp1[5]
    result = temp[1]
    ctrl_or_store = ''
    if pc in control_equiclass_map:
        ctrl_or_store = 'ctrl'
    elif pc in store_equiclass_map:
        ctrl_or_store = 'store'
    equiclass = (ctrl_or_store,pc,pilot,reg,bit)
    if 'Detected' in result:
        result = 'det'
    elif 'Mask' in result:
        result = 'mask'
    elif 'Tolerable' in result:
        result = 'sdc'
    if equiclass not in orig_outcomes_map:
        orig_outcomes_map[equiclass] = result

equiclass_map = {}
correct = 0
incorrect = 1
percent = 2

for outcome in outcomes:
    temp = outcome.split("::")
    inj = temp[0].split(',')
    result = temp[1]
    cycle = inj[cycle_idx]
    reg = inj[reg_idx]
    bit = inj[bit_idx]
    src_dest = inj[src_dest_idx]
    if cycle not in cycle_pc_map:
        continue
    pc = cycle_pc_map[cycle]

    ctrl_or_store = ""
    equiv_id = ""
    if pc in control_equiclass_map:
        ctrl_or_store = "ctrl"
        equiv_id = find_equiv_id(control_equiclass_map[pc], cycle)
    elif pc in store_equiclass_map:
        ctrl_or_store = "store"
        equiv_id = find_equiv_id(store_equiclass_map[pc], cycle)
    equiclass = (ctrl_or_store,pc,equiv_id,reg,bit)
    if equiclass not in equiclass_map:
        equiclass_map[equiclass] = [0]*3 # correct, incorrect, percent
    if 'Detected' in result:
        result = 'det'
    elif 'Mask' in result:
        result = 'mask'
    elif 'Tolerable' in result:
        result = 'sdc'
    if equiclass not in orig_outcomes_map:
        a = 1
    orig_result = orig_outcomes_map[equiclass]
    if result == orig_result:
        equiclass_map[equiclass][correct] += 1
    else:
        equiclass_map[equiclass][incorrect] += 1
    equiclass_map[equiclass][percent] = equiclass_map[equiclass][correct]/\
                                        float(sum(equiclass_map[equiclass][:2]))
 
outfile = app_prefix + '_validation_stats.csv' 
with open(outfile,'w') as f:
    f.write('ctrl_or_store,pc,pilot,reg,bit,correct,incorrect,percent\n')
    for equiclass in equiclass_map:
        counts = equiclass_map[equiclass]
        f.write("%s,%d,%d,%f\n" % (','.join(equiclass), counts[correct], counts[
                                  incorrect],counts[percent]))
