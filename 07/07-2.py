from itertools import permutations
from typing import *


class Amplifier:
    """A class for running the code of an amplifier."""

    def __init__(self, INST: List[int]):
        self.ip = 0
        self.inst = [i for i in INST]

    def run(self, input_value, phase=-1):
        """Run the amplifier with the specified value, returning None if it terminated
        and the value if it returned something."""
        # simplify the code
        ip = self.ip
        inst = self.inst

        while inst[ip] != 99:
            opt = inst[ip] % 100

            m1 = (inst[ip] // 100) % 10
            m2 = (inst[ip] // 1000) % 10

            if opt == 3:  # input
                # give it a phase if there is one, then the input value
                if phase != -1:
                    inst[inst[ip + 1]] = phase
                    phase = -1
                else:
                    inst[inst[ip + 1]] = input_value

                ip += 2

            elif opt == 4:  # output
                self.ip = ip + 2
                return inst[inst[ip + 1]] if m1 == 0 else inst[ip + 1]

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
                    ip = v2 if (v1 != 0) else (ip + 3)

                elif opt == 6:  # jump-if-false
                    ip = v2 if (v1 == 0) else (ip + 3)

                elif opt == 7:  # less than
                    inst[inst[ip + 3]] = 1 if v1 < v2 else 0
                    ip += 4

                elif opt == 8:  # equals
                    inst[inst[ip + 3]] = 1 if v1 == v2 else 0
                    ip += 4

        return None


INST = list(map(int, open("07.in", "r").read().strip().split(",")))

# try out all the permutations
max_input_value = 0
for perm in permutations((5, 6, 7, 8, 9)):
    amplifiers = [Amplifier(INST) for _ in range(5)]

    # run the initial input with phases
    input_value = 0
    i = 0
    while i < 5:
        input_value = amplifiers[i % 5].run(input_value, perm[i])
        i += 1

    while len(amplifiers) != 0:
        result = amplifiers[i % 5].run(input_value)

        # if any halts, break
        if result is None:
            # possibly check for higher output value
            if input_value > max_input_value:
                max_input_value = input_value

            break

        input_value = result
        i += 1

print(max_input_value)
