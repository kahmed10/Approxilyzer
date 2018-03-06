#!/usr/bin/python
import random
import sys

class basic_block:
    def __init__(self,bb_id,tick_start):
        self.bb_id = bb_id
        self.tick_start = tick_start
        self.store_addr_map = {}
        self.has_stores = False

class st_inst:
    def __init__(self,addr,tick):
        self.addr = addr
        self.tick = tick
        self.loads = []
    def add_load(self,load_pc):
        self.loads.append(load_pc)

# get information of the program counter

if len(sys.argv) != 2:
    print("Usage: python store_equivalence.py [app_name]")
    exit()

app_name = sys.argv[1]


pc_fname = app_name + "_parsed.txt"
mem_fname = app_name + "_clean_dump_parsed_merged.txt"



pc_fname_list = open(pc_fname).read().splitlines()
pc_control_map = {}
for line in pc_fname_list[1:]: # first line in file is a header
    temp = line.split()
    pc = temp[0]
    ctrl_flag = temp[2]
    pc_control_map[pc] = ctrl_flag == "True"


del pc_fname_list




# get information about the time clocks
ins_file_list = open(mem_fname).read().splitlines()

ins_content = [x.strip().split() for x in ins_file_list] 

del ins_file_list

print('Number of ticks', len(ins_content))
print('Number of PCs', len(pc_control_map))





# TODO: legacy implementation, enforce clean version automatically
# remove the ticks not present in PC Key (library access etc)
#trace_list = [item for item in ins_content if item[1][2:] in pc_key] # 2: here gets rid of 0x
trace_list = ins_content

# find basic blocks
ctrl_inst_index = [i for i in range(len(trace_list)) if pc_control_map[trace_list[i][1][2:]]] # index for control instructions

basicblocks = set() # set of basic block ids 2-length tuple with first element as start PC and second as end PC
program_bb = [] # program represented as basic blocks with tick value at start of basic block
bb_map = {} # map bbs to id
tick_starts = set() # used to check start of new bb

def add_bb(bb_start, bb_end, tick):
    global basicblocks
    global program_bb
    global bb_map
    global tick_starts
    
    tick_starts.add(tick)
    bb_id = (bb_start,bb_end)
    if bb_id not in basicblocks:
        basicblocks.add(bb_id)
        bb_map[bb_id] = []
    bb = basic_block(bb_id,tick)
    program_bb.append(bb)
    bb_map[bb_id].append(bb)
    

for index in range(len(ctrl_inst_index)-1):
    # check if there are PCs between two control instructions
    if index == 0:
        ctrl_start = ctrl_inst_index[0]
        if ctrl_start > 1: # create first bb from the beginning tick
            bb_start = trace_list[0][1][2:]
            bb_end = trace_list[ctrl_start-1][1][2:]
            tick = int(trace_list[0][0])
            add_bb(bb_start, bb_end, tick)
            
    if ctrl_inst_index[index+1] - ctrl_inst_index[index] >= 2:
        bb_start = trace_list[ctrl_inst_index[index] + 1][1][2:]
        bb_end = trace_list[ctrl_inst_index[index+1] - 1][1][2:]
        tick = int(trace_list[ctrl_inst_index[index] + 1][0])
        add_bb(bb_start, bb_end, tick)

# instructions after the last control block are to be included; the last instruction probably is a control instruction though.        
print("Basic blocks created.")

bb_index = -1
for item in trace_list:
    tick = int(item[0])
    addr = item[-1]
    pc = item[1][2:]
    if not pc_control_map[pc]:
        if tick in tick_starts:
            bb_index += 1
        if len(item) == 4:  # ld/st instruction
            if item[-2] == "Write":
                try:  # debugging
                    if addr not in program_bb[bb_index].store_addr_map:
                        program_bb[bb_index].store_addr_map[addr] = []
                    program_bb[bb_index].store_addr_map[addr].append(
                            st_inst(addr,tick))
                except:
                    print("bb_index: %d" % bb_index)
            elif item[-2] == "Read":
                try:
                    if addr in program_bb[bb_index].store_addr_map:
                        num_stores = len(program_bb[bb_index].store_addr_map[
                                addr])
                        for i in range(num_stores,0,-1):
                            curr_st_inst = program_bb[bb_index].store_addr_map[
                                addr][i-1]
                            # get most recent store
                            if tick > curr_st_inst.tick:
                                curr_st_inst.add_load(pc)
                                break
                except:
                    print("bb_index: %d" % bb_index)
print("Loads and stores populated")
total_classes = 0
total_ticks = 0
output_filename = "%s_store_equivalence.txt" % app_name
output_file = open(output_filename, "wb")
for bb_id in basicblocks:
    for j in range(len(bb_map[bb_id][0].store_addr_map)):
        addr_list = bb_map[bb_id][0].store_addr_map.keys()
        for k in range(len(bb_map[bb_id][0].store_addr_map[addr_list[j]])):
            store_equiv_map = {}
            for i in range(len(bb_map[bb_id])):
                addr_list = bb_map[bb_id][i].store_addr_map.keys()
                curr_st_inst = bb_map[bb_id][i].store_addr_map[
                    addr_list[j]][k]
                ld_pc_pattern = "".join(curr_st_inst.loads)
                if ld_pc_pattern != "":
                    if ld_pc_pattern not in store_equiv_map:
                        store_equiv_map[ld_pc_pattern] = []
                    store_equiv_map[ld_pc_pattern].append(curr_st_inst.tick)
            for ld_pc_pattern in store_equiv_map:
                store_equiclass = "%s:" % store_equiv_map[ld_pc_pattern][0]
                store_equiclass += "%d:" % len(store_equiv_map[
                    ld_pc_pattern])
                for tick in store_equiv_map[ld_pc_pattern]:
                    store_equiclass += " %s" % tick
                    total_ticks += 1
                total_classes += 1
                output_file.write("%s\n" % store_equiclass)
output_file.close()

print("Total classes: %d" % total_classes)
print("Total ticks in file: %d" % total_ticks)
