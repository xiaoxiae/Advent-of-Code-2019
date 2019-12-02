inst = list(map(int, open("02.in", "r").read().strip().split(",")))
ip = 0

inst[1] = 12
inst[2] = 2

while inst[ip] != 99:
    if inst[ip] == 1:
        inst[inst[ip + 3]] = inst[inst[ip + 1]] + inst[inst[ip + 2]]

    else:
        inst[inst[ip + 3]] = inst[inst[ip + 1]] * inst[inst[ip + 2]]

    ip += 4

print(inst[0])
