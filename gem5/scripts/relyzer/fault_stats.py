
# coding: utf-8

# In[59]:
import sys

if len(sys.argv) != 2:
    print("Usage: python equivalence_class.py [app_name]")
    exit()
app_name = sys.argv[1]
# pc_fname = app_name + "_parsed.txt"



#app_name = 'lu'   # 'fft', 'lu' are the two options
#if app_name in 'fft':
#    finj_fname = 'fft_ec_output.txt'
#elif app_name in 'lu':
#    finj_fname = 'lu_ec_output.txt'
finj_fname = app_name+"_ec_output.txt"
#else:
#    print('Invalid application name')


with open(finj_fname) as f:
    finj_content = f.readlines()

finj_content = [x.strip().split(',') for x in finj_content] 
finj_content = [item[0:5] + item[5].split('::') for item in finj_content]


# In[60]:


fault_stats_map_key = set(["%s,%s,%s,%s" % (item[0],item[1],item[3],item[4]) for item in finj_content]) # create a map with key - equivalence class,reg,bit
for i in range(len(finj_content)):
    if "Detected" in finj_content[i][-1]:
        finj_content[i][-1] = "Detected"

unique_faults = list(set([item[-1] for item in finj_content]))
fault_ind = {unique_faults[i]:i for i in range(0,len(unique_faults))} # find unique faults and create a map to get an index corresponding to each fault

fault_stats_map = {key:[0]*len(unique_faults) for key in fault_stats_map_key} # stores a list for each unique key, list has the frequency counts of each detected fault

# populate the fault_stats_map
for item in finj_content:
    tempkey = "%s,%s,%s,%s" % (item[0],item[1],item[3],item[4])
    fault_stats_map[tempkey][fault_ind[item[-1]]] += 1



# make a list with ec,reg,bit,array,max percentage to print into CSV file
#import pdb; pdb.set_trace()
csvlist = []
for item in fault_stats_map:
    item_spl = item.split(',')
    tpl = fault_stats_map[item]
    tempmaxperc = max(tpl)/float(sum(tpl))
    tempappend = [item_spl[0], item_spl[1], item_spl[2], item_spl[3], tpl[0], tpl[1], tpl[2], tempmaxperc]
    csvlist.append(tempappend)


csvfilename = app_name+'_ec_stats.csv'
csvfile = open(csvfilename, 'w')

for sublist in csvlist:
    csvfile.write("%s,%s,%s,%s,%s,%s,%s,%s\n" %(sublist[0], sublist[1],sublist[2],sublist[3],sublist[4],sublist[5],sublist[6],sublist[7]))

csvfile.close()

#import pdb
#pdb.set_trace()

# In[61]:


# table_columns = [[] for i in range(0, len(unique_faults))]
# for key in fault_stats_map_key:
#     for ft in unique_faults:
#         table_columns[fault_ind[ft]].append(fault_stats_map[key][fault_ind[ft]])

# use table_columns to create a table with the astropy.tables package

