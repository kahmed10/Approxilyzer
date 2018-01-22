
# coding: utf-8

# In[197]:


# this file is to create blocks
# import matplotlib.pyplot as plt
# import numpy as np
import random
import sys

# In[198]:


# get information of the program counter

if len(sys.argv) != 2:
    print("Usage: python equivalence_class.py [app_name]")
    exit()

app_name = sys.argv[1]


pc_fname = app_name + "_parsed.txt"
ins_fname = app_name + "_dump_parsed.txt"


# app_name = 'fft'   # 'fft', 'lu' are the two options
# if app_name in 'fft':
#     pc_fname = 'fft_parsed.txt'
#     ins_fname = 'fft_dump_parsed.txt'
# elif app_name in 'lu':
#     pc_fname = 'lu_cb_parsed.txt'
#     ins_fname = 'lu_dump_parsed.txt'    
# else:
#     print('Invalid application name')


# with open(pc_fname) as f:
#     pc_content = f.readlines()

pc_fname_list = open(pc_fname).read().splitlines()

pc_content = [line.split() for line in pc_fname_list[1:]]

del pc_fname_list


#pc_content = [x.strip().split() for x in pc_content[1:]] 


# get information about the time clocks
with open(ins_fname) as f:
    ins_content = f.readlines()

ins_file_list = open(ins_fname).read().splitlines()

ins_content = [x.strip().split() for x in ins_file_list] 

del ins_file_list

print('Number of ticks', len(ins_content))
print('Number of PCs', len(pc_content))


# In[199]:


# create a map which can be keyed with PC value to find whether instruction is control or not
pc_key = [item[0] for item in pc_content]
pc_control_map = {}
for pc in pc_key:
    pc_control_map[pc] = []

for pc in pc_control_map:
    cflag = [item[2] for item in pc_content if item[0] == pc]
    if cflag[0] == 'True':
        pc_control_map[pc].append(1) # append 1 if it is a control instruction
    else:
        pc_control_map[pc].append(0) # appned 0 if it is not a control instruction


# In[200]:


# remove the ticks not present in PC Key (library access etc)
tick_pc_list = [item for item in ins_content if item[1][2:] in pc_key] # 2: here gets rid of 0x


# In[201]:


# find basic blocks
conins_index = [i for i in range(0,len(tick_pc_list)) if pc_control_map[tick_pc_list[i][1][2:]][0] == 1] # index for control instructions

basicblocks = [] # list of basic blocks. Each list element is a 2-length list with first element as start PC and second as end PC
program_bb = [] # program represented as basic blocks with tick value at start of basic block

for cind in range(0,len(conins_index)-1):
    if conins_index[cind+1] - conins_index[cind] >= 2: # check if there are PCs between two control instructions
        bbstart = tick_pc_list[conins_index[cind] + 1][1][2:]
        bbend = tick_pc_list[conins_index[cind+1] - 1][1][2:]
        
        if [str(bbstart), str(bbend)] not in basicblocks: # check if this basic block is new
            basicblocks.append([str(bbstart), str(bbend)])
            
        bbnum = [i for i in range(0,len(basicblocks)) if [str(bbstart), str(bbend)] == basicblocks[i]]
        if len(bbnum)>1:
                print('Repeat entry in basicblocks')
        tickval = int(tick_pc_list[conins_index[cind] + 1][0])
        program_bb.append([tickval, bbnum[0]])

# instructions after the last control block are to be included; the last instruction probably is a control instruction though.        
print('Basic blocks created.')
print(len(tick_pc_list), conins_index[-1])


# In[202]:


# create equivalence classes and find their ticks
equiclass_depth = 50    # length of elements in equivalent class
equiclass_list = []   # list of equivalent classes
equiclass_ticks = []  # start times corresponding to each equivalent class instance

for index in range(0,len(program_bb)-equiclass_depth+1):
    bbseq = [item[1] for item in program_bb[index:index+equiclass_depth]]
    tickval = program_bb[index][0]
    if bbseq not in equiclass_list:
        equiclass_list.append(bbseq)
    equiclass_num = [i for i in range(0,len(equiclass_list)) if bbseq == equiclass_list[i]]
    if len(equiclass_num)>1:
        print('Repeat entry in equiclass_list')
        
    if equiclass_num[0] == len(equiclass_ticks):
        equiclass_ticks.append([])

    equiclass_ticks[equiclass_num[0]].append(tickval)

print('Equivalence classes created.')


# In[203]:


count_per_equiclass = [len(sublist) for sublist in equiclass_ticks]  
# plt.plot(count_per_equiclass)
# plt.show()


# In[204]:


print('Program length in bbs:', len(program_bb))
print('Number of basic blocks:', len(basicblocks))
print('Number of equivalence classes:', len(equiclass_list))
print('Most frequent equivalence class count:', max(count_per_equiclass))

maxind = [i for i in range(0, len(count_per_equiclass)) if count_per_equiclass[i]==max(count_per_equiclass)]
print('Equivalent classes with max occurence:', maxind)


# In[205]:


# each element of the list bbreginfo corresponds to one basic block. That element is made of a list of two elements
# (i) the set of registers invoked in the basic block
# (ii) list of list of location wrt to start PC of the basic block where register is invoked

bbreginfo = []
for bbi in range(0,len(basicblocks)):
    bbstart_index = [i for i in range(0,len(pc_content)) if pc_content[i][0] == basicblocks[bbi][0]][0]
    bbend_index = [i for i in range(0,len(pc_content)) if pc_content[i][0] == basicblocks[bbi][1]][0]
    
    reglist=[item[3].split(',') for item in pc_content[bbstart_index:bbend_index+1]]
    unireg = list(set([item for sublist in reglist for item in sublist]))
    if 'None' in unireg:
        unireg.remove('None')

    register_loc = []
    for rg in unireg:
        rgind = [i for i in range(0,len(reglist)) if rg in reglist[i]]
        register_loc.append(rgind)

    bbreginfo.append([unireg, register_loc])
    


# In[206]:


# output the register and the time tick at which fault injection is to be done
frequent_ec = [i for i in range(0,len(equiclass_list)) if count_per_equiclass[i]>=10] # KHALIQUE: changing to 10 for now...

# print('Ecs with more than 2 occurences:', frequent_ec)
#print(frequent_ec)

tick_reg_inject_list = []
tick_ec_inject_list = []

for equic in frequent_ec:
    #start_tick = equiclass_ticks[equic] # start ticks for basic block / equivalence class
    # SELECTING ONE RANDOM TICK
    temp_list = equiclass_ticks[equic]
    random.shuffle(temp_list)
    start_tick = []

    for i in range(10):
        start_tick.append(temp_list[i])

    #start_tick = [random.choice(equiclass_ticks[equic])]
    start_tick_index = [i for i in range(0,len(tick_pc_list)) if int(tick_pc_list[i][0]) in start_tick]
    bbinject = equiclass_list[equic][0] # basic block number
    bbreg = bbreginfo[bbinject] # register information for the basic block
    
    if len(bbreg[0]) > 0:
        for i in range(0, len(bbreg[0])):
            reg_name = bbreg[0][i]
            inject_tick_list = [tind+rind for tind in start_tick_index for rind in bbreg[1][i]]

            for itl in inject_tick_list:
                tick_reg_inject_list.append([int(tick_pc_list[itl][0]), reg_name]) # tick-register
                tick_ec_inject_list.append([equic, int(tick_pc_list[itl][0]), tick_pc_list[itl][1]]) # equivalence class-tick-PC
    else:
        print(equic)
print('Number of tick-registers pairs:', len(tick_reg_inject_list))


# In[207]:


# write the tick-register pairs from tick_reg_inject_list into a text file
trifilename = app_name+'_tick_reg_list.txt'
trifile = open(trifilename, 'w')

for sublist in tick_reg_inject_list:
    trifile.write("%s,%s\n" %(sublist[0], sublist[1]))

trifile.close()

etpcfilename = app_name+'_ec_tick_pc_list.txt'
etpcfile = open(etpcfilename, 'w')

for sublist in tick_ec_inject_list:
    etpcfile.write("%s,%s,%s\n" %(sublist[0], sublist[1], sublist[2]))

etpcfile.close()


# In[208]:


# rough code for checking

