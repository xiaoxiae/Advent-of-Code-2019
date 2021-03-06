inst = list(map(int, open("05.in", "r").read().strip().split(",")))
ip = 0
input_value = 5

while inst[ip] != 99:
    opt = inst[ip] % 100

    m1 = (inst[ip] // 100) % 10
    m2 = (inst[ip] // 1000) % 10

    if opt == 3:  # input
        inst[inst[ip + 1]] = input_value
        ip += 2

    elif opt == 4:  # output
        print(inst[inst[ip + 1]] if m1 == 0 else inst[ip + 1])
        ip += 2

    else:
        v1 = inst[inst[ip + 1]] if (inst[ip] // 100) % 10 == 0 else inst[ip + 1]
        v2 = inst[inst[ip + 2]] if (inst[ip] // 1000) % 10 == 0 else inst[ip + 2]

        if opt == 1:  # addition
            inst[inst[ip + 3]] = v1 + v2
            ip += 4

        elif opt == 2:  # multiplication
            inst[inst[ip + 3]] = v1 * v2
            ip += 4

        elif opt == 5:  # jump-if-true
            ip = v2 if (v1 != 0) else ip + 3

        elif opt == 6:  # jump-if-false
            ip = v2 if (v1 == 0) else ip + 3

        elif opt == 7:  # less than
            inst[inst[ip + 3]] = 1 if v1 < v2 else 0
            ip += 4

        elif opt == 8:  # equals
            inst[inst[ip + 3]] = 1 if v1 == v2 else 0
            ip += 4
