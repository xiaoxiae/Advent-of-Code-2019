inst = [0]
for n in range(99):
    for v in range(99):
        inst = list(map(int, open("02.in", "r").read().strip().split(",")))
        ip = 0

        inst[1] = n
        inst[2] = v

        while inst[ip] != 99:
            if inst[ip] == 1:
                inst[inst[ip + 3]] = inst[inst[ip + 1]] + inst[inst[ip + 2]]

            else:
                inst[inst[ip + 3]] = inst[inst[ip + 1]] * inst[inst[ip + 2]]

            ip += 4

        if inst[0] == 19690720:
            print(100 * n + v)
            exit()
