#!/usr/bin/python

import os
import sys

if len(sys.argv) != 3:
    print("Usage: python validation_aggregate_stats.py" + \
          " [app] [isa]")
    exit()
app_name = sys.argv[1]
isa = sys.argv[2]

approx_dir = os.environ.get('APPROXGEM5')
apps_dir = approx_dir + '/workloads/' + isa + '/apps/' + app_name
app_prefix = apps_dir + '/' + app_name

ctrl_file = app_prefix + '_final_control_equivalence.txt'
store_file = app_prefix + '_final_store_equivalence.txt'
stats_file = app_prefix + '_validation_stats.csv'

ctrl_pilot_map = {i.split(':')[2]:int(i.split(':')[1]) for i in open(
                    ctrl_file).read().splitlines()[1:]}
store_pilot_map = {i.split(':')[2]:int(i.split(':')[1]) for i in open(
                    store_file).read().splitlines()[1:]}

stats_list = [i.split(',') for i in open(
                    stats_file).read().splitlines()[1:]]

store_weighted_sum = 0
store_total_pop = 0
ctrl_weighted_sum = 0
ctrl_total_pop = 0
for item in stats_list:
    ctrl_or_store = item[0]
    pilot = item[2]
    accuracy = float(item[7])
    pop = 0
    if ctrl_or_store == 'store':
        pop = store_pilot_map[pilot]
        store_weighted_sum += pop*accuracy
        store_total_pop += pop 
    else:
        pop = ctrl_pilot_map[pilot]
        ctrl_weighted_sum += pop*accuracy
        ctrl_total_pop += pop 

store_weighted_average = store_weighted_sum / store_total_pop
ctrl_weighted_average = ctrl_weighted_sum / ctrl_total_pop
print('store_weighted_average: %f' % store_weighted_average)
print('ctrl_weighted_average: %f' % ctrl_weighted_average)
    
