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
f = open(sys.argv[1], 'rb')
wf = open(sys.argv[2],'w')
wf.write('PC OP CONTROL_FLAG SRC_REG\n')

for line in f:
    line = line[:9] + line[31:]
    if valid_pattern.match(line) and '(bad)' not in line:
        data = line[2:].rstrip('\r\n').split(':	')
        pc = data[0]
        #op = data[1].split('\t')[1].split()[0]
        op = data[1].split(' ', 1)[0]
        #op = data[1].split(' ', 1)[0]
        reg = []
        if '.' in op:
            try:
                op = data[1].split(' ', 1)[1].split(' ')[0]
                reg_info = data[1].split(' ', 1)[1].split(' ')[1]
            except:
                continue
        elif len(data[1].split(' ', 1)) > 1:
            reg_info = data[1].split(' ', 1)[1]
        comma_split = reg_info.lstrip().split(',')
        src_exist = False
        if len(comma_split) == 1:
            src_reg = 'None'
        elif len(comma_split) == 2:
            src_info = comma_split[0]
            for pattern in reg_pattern:
                p = re.compile(pattern)
                match = p.search(src_info)
                if type(match) != NoneType:
                    src_exist = True
                    src_reg = match.group(0).lstrip('%')
        elif len(comma_split) == 3:
            src_info = comma_split[1]
            for pattern in reg_pattern:
                p = re.compile(pattern)
                match = p.search(src_info)
                if type(match) != NoneType:
                    src_exist = True
                    src_reg = match.group(0).lstrip('%')
        if not src_exist:
            src_reg = 'None'

        writeln = pc + ' ' + op + ' '
        writeln += 'True ' if isControlInstruction(op) else 'False '
        writeln += src_reg + '\n'
        wf.write(writeln)
        #print writeln.rstrip(',')
        #print pc, op, reg, control_op
