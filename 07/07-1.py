from itertools import permutations

INST = list(map(int, open("07.in", "r").read().strip().split(",")))

# try out all the permutations
max_input_value = 0
for perm in permutations((0, 1, 2, 3, 4)):

    input_value = 0
    for phase in perm:

        inst = [i for i in INST]
        ip = 0

        while inst[ip] != 99:
            opt = inst[ip] % 100

            m1 = (inst[ip] // 100) % 10
            m2 = (inst[ip] // 1000) % 10

            if opt == 3:  # input
                pos = inst[ip + 1] if m1 == 0 else ip + 1

                # give it a phase first and the input value second
                if phase != -1:
                    inst[pos] = phase
                    phase = -1
                else:
                    inst[pos] = input_value

                ip += 2

            elif opt == 4:  # output
                input_value = inst[inst[ip + 1]] if m1 == 0 else inst[ip + 1]
                ip += 2

            else:
                # parameter parsing (by modes)
                v1 = inst[inst[ip + 1]] if m1 == 0 else inst[ip + 1]
                v2 = inst[inst[ip + 2]] if m2 == 0 else inst[ip + 2]

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

        if max_input_value < input_value:
            max_input_value = input_value

print(max_input_value)
