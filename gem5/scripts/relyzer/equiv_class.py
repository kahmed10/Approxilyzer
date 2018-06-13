#!/usr/bin/python

# equivalence class data structure (currently used in store_equivalence.py
# and postprocessing.py, TODO: use in control_equivalence.py)
import random


class equiv_class(object):
    def __init__(self,pc,in_string=None):
        '''
        initializes equivalence class data structure (use in_string to read
        existing data from file)
        '''
        if in_string is None:
            self.pc = pc
            self.members = []
            self.pop = 0
            self.pilot = None
        else:
            temp = in_string.split(':')
            self.pc = temp[0]
            self.pop = int(temp[1])
            self.pilot = temp[2]
            self.members = temp[3].lstrip().split()

    def add_member(self,inst_num):
        '''
        adds a member to the equivalence class
        Args: isnt_num - instruction number of dynamic PC to add
        '''
        self.members.append(inst_num)
        self.pop += 1
    
    def remove_member(self,inst_num):
        '''
        removes a member from the equivalence class (to save space).
        Args: inst_num - instruction number of dynamic PC to remove
        '''
        if inst_num in self.members:
            self.members.remove(inst_num)
            self.pop -= 1

    def select_pilot(self,seed_val=1):
        '''
        selects a pilot from the list of members at random.
        Args: (Optional) seed_val - used for making sure pilot selection
        is deterministic
        '''
        random.seed(seed_val)
        if len(self.members) > 0:
            rand_pilot_idx = random.randint(0,len(self.members)-1)
            self.pilot = self.members[rand_pilot_idx]

    def print_equiv_class(self):
        '''
        prints the given equivalence class.
        Returns: output - string of all contents of the equivalence class
        '''
        output = '%s:%d:%s:%s' % (self.pc, self.pop, self.pilot, \
                 ' '.join(self.members))
        return output

class equiv_class_database(object):
    def __init__(self, filename):
        '''
        creates a database depending on equiv class file (ctrl or store)
        '''
        equiv_class_list = open(filename).read().splitlines()[1:]
        self.equiv_class_map = {}
        equiv_classes = []

        for item in equiv_class_list:
            equiv_classes.append(equiv_class(None,in_string=item))
        for _equiv_class in equiv_classes:
            for member in _equiv_class.members:
                self.equiv_class_map[member] = _equiv_class.pilot
    
    def get_pilot(self, inst_num):
        '''
        gets the pilot of the appropriate equiv class (if it exists)
        '''
        return self.equiv_class_map.get(inst_num, None)
