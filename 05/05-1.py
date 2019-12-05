inst = list(map(int, open("05.in", "r").read().strip().split(",")))
ip = 0
input_value = 1

while inst[ip] != 99:
    opt = inst[ip] % 100

    if opt == 3:  # input
        inst[inst[ip + 1]] = input_value
        ip += 2

    elif opt == 4:  # output
        print(inst[inst[ip + 1]])
        ip += 2

    else:
        # parameter parsing (by modes)
        v1 = inst[inst[ip + 1]] if (inst[ip] // 100) % 10 == 0 else inst[ip + 1]
        v2 = inst[inst[ip + 2]] if (inst[ip] // 1000) % 10 == 0 else inst[ip + 2]

        if opt == 1:  # addition
            inst[inst[ip + 3]] = v1 + v2

        else:  # multiplication
            inst[inst[ip + 3]] = v1 * v2

        ip += 4
