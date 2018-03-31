import sys

term_output = open(sys.argv[1]).read().splitlines()

started = False

output = []
for line in term_output:
    if "STARTING" and "STOPPING" not in line:
        if "STOPPING" in line:
            break
        if "No such file or directory" in line:
            exit()
        if started:
            output.append(line)
        if "STARTING" in line:
            started = True

for line in output:
    print(line)
