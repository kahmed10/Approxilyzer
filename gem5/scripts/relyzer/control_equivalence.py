#!/usr/bin/python
import random
import sys



# get information of the program counter

if len(sys.argv) != 2:
    print("Usage: python control_equivalence.py [app_name]")
    exit()

app_name = sys.argv[1]


pc_fname = app_name + "_parsed.txt"
ins_fname = app_name + "_clean_dump_parsed_merged.txt"



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




# remove the ticks not present in PC Key (library access etc)
tick_pc_list = ins_content  #[item for item in ins_content if item[1][2:] in pc_key] # 2: here gets rid of 0x




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
        tick_val = int(tick_pc_list[conins_index[cind] + 1][0])
        program_bb.append([tick_val, bbnum[0]])

# instructions after the last control block are to be included; the last instruction probably is a control instruction though.        
print('Basic blocks created.')
#print(len(tick_pc_list), conins_index[-1])




# create equivalence classes and find their ticks
equiclass_depth = 50    # length of elements in equivalence class
equiclass_cap = 50 # cap on number of equivalence classes per basic block
equiclass_map = {}   # list of equivalence classes
equiclass_index_map = {} # stores indices for members of equivalence class
equiclass_ticks_map = {}  # start times corresponding to each equivalence class instance
equiclass_bb_count = {}

def create_equiclass(bbseq, tick_val, index, bb_id):
    global equiclass_map
    global equiclass_index_map
    global equiclass_ticks_map
    global equiclass_bb_count

    equiv_match = False

    if bb_id not in equiclass_map:
        equiclass_map[bb_id] = {}
        equiclass_index_map[bb_id] = {}
        equiclass_ticks_map[bb_id] = {}
    for equiv_id in equiclass_map[bb_id]: 
        if bbseq == equiclass_map[bb_id][equiv_id]:
            equiv_match = True
            equiclass_index_map[bb_id][equiv_id].append(index)
            equiclass_ticks_map[bb_id][equiv_id].append(tick_val)
            break
    if not equiv_match:
        equiclass_map[bb_id][index] = bbseq
        equiclass_index_map[bb_id][index] = [index]
        equiclass_ticks_map[bb_id][index] = [tick_val]
        equiv_id = index


    # check number of equiclasses for each bb
    if bb_id not in equiclass_bb_count:
        equiclass_bb_count[bb_id] = set()
    equiclass_bb_count[bb_id].add(equiv_id)



for main_index in range(0,len(program_bb)-equiclass_depth+1):
    index = main_index # distinguishing main_index from index for clarity
    bbseq = [item[1] for item in program_bb[index:index+equiclass_depth]]
    tick_val = program_bb[index][0]
    bb_id = program_bb[index][1]
    create_equiclass(bbseq, tick_val, index, bb_id)
    
#     if bb_id not in equiclass_map:
#         equiclass_map[bb_id] = {}
#         equiclass_index_map[bb_id] = {}
#         equiclass_ticks_map[bb_id] = {}
#     for equiv_id in equiclass_map[bb_id]: 
#         if bbseq == equiclass_map[bb_id][equiv_id]:
#             equiv_match = True
#             equiclass_index_map[bb_id][equiv_id].append(index)
#             equiclass_ticks_map[bb_id][equiv_id].append(tick_val)
#             break
#     if not equiv_match:
#         equiclass_map[bb_id][index] = bbseq
#         equiclass_index_map[bb_id][index] = [index]
#         equiclass_ticks_map[bb_id][index] = [tick_val]
#         equiv_id = index
# 
# 
#     # check number of equiclasses for each bb
#     if bb_id not in equiclass_bb_count:
#         equiclass_bb_count[bb_id] = set()
#     equiclass_bb_count[bb_id].add(equiv_id)
    
    # dynamically resize until the number of equivalence classes within cap
    if len(equiclass_bb_count[bb_id]) > equiclass_cap:
        total_indices = []
        for equiv_id in equiclass_index_map[bb_id]:
             for index in equiclass_index_map[bb_id][equiv_id]:
                total_indices.append(index)

        new_depth = equiclass_depth - 1
        while len(equiclass_bb_count[bb_id]) > equiclass_cap:
            # reset data structures associated with bb_id
            equiclass_map[bb_id] = {}
            equiclass_index_map[bb_id] = {}
            equiclass_ticks_map[bb_id] = {}
            equiclass_bb_count[bb_id] = set()
            
            for index in total_indices:
                 
                bbseq = [item[1] for item in program_bb[index:index+new_depth]]
                tick_val = program_bb[index][0]
                
                create_equiclass(bbseq, tick_val, index, bb_id)
                
#                 for equiv_id in equiclass_map[bb_id]: 
#                     if bbseq == equiclass_map[bb_id][equiv_id]:
#                         equiv_match = True
#                         equiclass_index_map[bb_id][equiv_id].append(index)
#                         equiclass_ticks_map[bb_id][equiv_id].append(tick_val)
#                         break
#                 if not equiv_match:
#                     equiclass_map[bb_id][index] = bbseq
#                     equiclass_index_map[bb_id][index] = [index]
#                     equiclass_ticks_map[bb_id][index] = [tick_val]
#                     equiv_id = index
# 
#                 equiclass_bb_count[bb_id].add(equiv_id)
            new_depth -= 1
#    print("Finished iteration: %d" % index)    

# edge case towards the end of the array
for main_index in range(len(program_bb)-equiclass_depth,len(program_bb)):
    end_depth = len(program_bb)-(len(program_bb)-equiclass_depth)
    index = main_index # distinguishing main_index from index for clarity
    bbseq = [item[1] for item in program_bb[index:index+end_depth]]
    tick_val = program_bb[index][0]
    bb_id = program_bb[index][1]

    create_equiclass(bbseq, tick_val, index, bb_id)
    
#     if bb_id not in equiclass_map:
#         equiclass_map[bb_id] = {}
#         equiclass_index_map[bb_id] = {}
#         equiclass_ticks_map[bb_id] = {}
#     for equiv_id in equiclass_map[bb_id]: 
#         if bbseq == equiclass_map[bb_id][equiv_id]:
#             equiv_match = True
#             equiclass_index_map[bb_id][equiv_id].append(index)
#             equiclass_ticks_map[bb_id][equiv_id].append(tick_val)
#             break
#     if not equiv_match:
#         equiclass_map[bb_id][index] = bbseq
#         equiclass_index_map[bb_id][index] = [index]
#         equiclass_ticks_map[bb_id][index] = [tick_val]
#         equiv_id = index
# 
# 
#     # check number of equiclasses for each bb
#     if bb_id not in equiclass_bb_count:
#         equiclass_bb_count[bb_id] = set()
#     equiclass_bb_count[bb_id].add(equiv_id)
    
    # dynamically resize until the number of equivalence classes within cap
    if len(equiclass_bb_count[bb_id]) > equiclass_cap:
        total_indices = []
        for equiv_id in equiclass_index_map[bb_id]:
             for index in equiclass_index_map[bb_id][equiv_id]:
                total_indices.append(index)

        new_depth = end_depth - 1
        while len(equiclass_bb_count[bb_id]) > equiclass_cap:
            # reset data structures associated with bb_id
            equiclass_map[bb_id] = {}
            equiclass_index_map[bb_id] = {}
            equiclass_ticks_map[bb_id] = {}
            equiclass_bb_count[bb_id] = set()
            
            for index in total_indices:
                 
                bbseq = [item[1] for item in program_bb[index:index+new_depth]]
                tick_val = program_bb[index][0]
                create_equiclass(bbseq, tick_val, index, bb_id)
#                 equiv_id = None
#                 
#                 for equiv_id in equiclass_map[bb_id]: 
#                     if bbseq == equiclass_map[bb_id][equiv_id]:
#                         equiv_match = True
#                         equiclass_index_map[bb_id][equiv_id].append(index)
#                         equiclass_ticks_map[bb_id][equiv_id].append(tick_val)
#                         break
#                 if not equiv_match:
#                     equiclass_map[bb_id][index] = bbseq
#                     equiclass_index_map[bb_id][index] = [index]
#                     equiclass_ticks_map[bb_id][index] = [tick_val]
#                     equiv_id = index
# 
#                 equiclass_bb_count[bb_id].add(equiv_id)
            new_depth -= 1
#    print("Finished iteration: %d" % index)    
        
print('Equivalence classes created.')

print('Program length in bbs:', len(program_bb))
print('Number of basic blocks:', len(basicblocks))

pc_equiclass_map = {}
# pc -> equiclass_id: [ ticks belonging to that equiclass id ]



bb_idx = -1
for item in tick_pc_list:
    tick = item[0]
    pc = item[1][2:]
    if tick == program_bb[bb_idx+1][0]:
        bb_idx += 1
    if len(item) > 2:  # store inst check
        if item[2] == "Write":
            continue  # stores will be handled w/ store equiv
    bb_id = program_bb[bb_idx][1]
    if pc not in pc_equiclass_map:
        pc_equiclass_map[pc] = {program_bb[bb_idx][1]:[]}

    pc_equiclass_map[pc][bb_id].append(tick)

output_file = "%s_control_equivalence.txt" % app_name
output = open(output_file, "w")
output.write("pc:population:pilot:members\n")
pc_list = sorted(pc_equiclass_map.keys())
for pc in pc_list:
    ctrl_equiclass = "%s:" % pc
    for bb_id in pc_equiclass_map[pc]:
        tick_list = pc_equiclass_map[pc][bb_id]
        ctrl_equiclass += "%d:" % len(tick_list)
        rand_tick_idx = random.randint(0,len(tick_list)-1)
        rand_tick = tick_list[rand_tick_idx]
        ctrl_equiclass += "%s:" % rand_tick
        for tick in tick_list:
            ctrl_equiclass += " %s" % tick
        output.write("%s\n" % ctrl_equiclass)
output.close()
    

