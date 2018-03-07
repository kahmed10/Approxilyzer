import re
import sys

from types import NoneType

if len(sys.argv) != 3:
    print("Usage: python dis_parser.py [dis_file] [out_file]")
    exit()

def isControlInstruction(strin):
    return 'jmp' in strin or 'je' in strin or 'jn' in \
        strin or 'jg' in strin or 'ja' in strin or 'jl' in strin or \
        'jb' in strin or 'jo' in strin or 'jz' in strin or 'js' in strin \
        or 'call' in strin or 'loop' in strin or 'ret' in strin

single_ops = ['push', 'sar', 'sal', 'shl', 'shr']

valid_pattern = re.compile("^\s+[0-9a-fA-F]+:\s*[a-zA-Z]+.*")
reg_pattern = ['%ax', '%al', '%ah', '%rax', '%eax',
               '%bx', '%bl', '%bh', '%rbx', '%ebx',
               '%cx', '%cl', '%ch', '%rcx', '%ecx',
               '%dx', '%dl', '%dh', '%rdx', '%edx',
               '%si', '%rsi', '%esi',
               '%di', '%rdi', '%edi',
               '%r8', '%r9', '%r10', '%r11', '%r12', '%r13', '%r14', '%r15',
               '%xmm0', '%xmm1', '%xmm2', '%xmm3', '%xmm4', '%xmm5', '%xmm6',
               '%xmm13', '%xmm7', '%xmm8', '%xmm9', '%xmm10', '%xmm11', '%xmm12',
               '%xmm14', '%xmm15',
               '%fpr0', '%fpr1', '%fpr2', '%fpr3', '%fpr4', '%fpr5', '%fpr6',
               '%fpr7']
paren_match = re.compile('.*\(.*\).*')

reg_matches = []
for pattern in reg_pattern:
    reg_matches.append(re.compile(pattern))
    
def is_mem_access(search_string):
    '''
    Checks if substring is found within parenthesis, meaning it is a 
    memory access
    Args: search_string - string to search in
    Returns: True - is a memory access, False otherwise
    '''
    return paren_match.match(search_string) is not None
        
    

def find_reg(search_string):
    '''
    Iterates through possible registers, finds possible match
    Args: search_string - string that may contain register
    Returns: reg - string if register found, None otherwise
    '''
    reg = None
    for reg_match in reg_matches:
        match = reg_match.search(search_string)
        if match:
            reg = match.group(0).lstrip('%')
            break
    return reg
        

f = open(sys.argv[1], 'rb')
wf = open(sys.argv[2],'w')
wf.write('PC OP CONTROL_FLAG SRC_REG DEST_REG\n')

for line in f:
    line = line[:9] + line[31:]
    if valid_pattern.match(line) and '(bad)' not in line:
        data = line[2:].rstrip('\r\n').split(':	')
        pc = data[0]
        #op = data[1].split('\t')[1].split()[0]
        op = data[1].split(' ', 1)[0]
        #op = data[1].split(' ', 1)[0]
        reg = []
        src_reg = None
        dest_reg = None
        if '.' in op:
            try:
                op = data[1].split(' ', 1)[1].split(' ')[0]
                reg_info = data[1].split(' ', 1)[1].split(' ')[1]
            except:
                continue
        elif len(data[1].split(' ', 1)) > 1:
            reg_info = data[1].split(' ', 1)[1]
        comma_split = reg_info.lstrip().split(',')
        # in x86, the number of src/dest operands varies
        if len(comma_split) == 1:
            is_src_op = False
            # src register may be just single register
            for single_op in single_ops:
                if op in single_op:
                    is_src_op = True
                    src_info = comma_split[0]
                    src_reg = find_reg(src_info)
                    break
            if not is_src_op:
                if len(comma_split[0]) > 0:
                    dest_info = comma_split[0]
                    if not is_mem_access(dest_info):
                        dest_reg = find_reg(dest_info)
                
        elif len(comma_split) == 2:
            src_info = comma_split[0]
            dest_info = comma_split[-1]
            src_reg = find_reg(src_info)
            if not is_mem_access(dest_info):
                dest_reg = find_reg(dest_info)
        elif len(comma_split) == 3:
            src_info = comma_split[1]
            dest_info = comma_split[-1]
            src_reg = find_reg(src_info)
            if not dest_reg:
                dest_reg = find_reg(dest_info)
            
        if src_reg is None:
            src_reg = 'None'
        if dest_reg is None:
            dest_reg = 'None'

        writeln = pc + ' ' + op + ' '
        writeln += 'True ' if isControlInstruction(op) else 'False '
        writeln += src_reg + ' ' + dest_reg + '\n'
        wf.write(writeln)
wf.close()
