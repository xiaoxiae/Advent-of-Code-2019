from random import *
from typing import *


class Memory:
    """A class for working with the computer memory."""

    def __init__(self, inst: Dict[int, int]):
        self.inst = {}

        for i, instruction in enumerate(inst):
            self.inst[i] = instruction

    def __setitem__(self, i, item: int):
        """Set the memory at the specified index."""
        self.inst[i] = item

    def __getitem__(self, i):
        """Get the memory at the specified index (possibly generating more memory)."""
        if i not in self.inst:
            self.inst[i] = 0

        return self.inst[i]


class Computer:
    def __init__(self, inst):
        self.inst = Memory(inst)

    def run(self, input_value) -> Generator:
        """"""
        ip = 0
        base = 0
        inst = self.inst

        while inst[ip] != 99:
            opt = inst[ip] % 100

            # modes
            m1 = (inst[ip] // 100) % 10
            m2 = (inst[ip] // 1000) % 10
            m3 = (inst[ip] // 10000) % 10

            p1 = inst[ip + 1]
            v1 = inst[p1] if m1 == 0 else p1 if m1 == 1 else inst[base + p1]

            if opt == 3:  # input
                inst[p1 if m1 == 0 else p1 + base] = input_value
                ip += 2

            elif opt == 4:  # output
                yield v1
                ip += 2

            elif opt == 9:  # relative base adjustment
                base += v1
                ip += 2

            else:
                p2 = inst[ip + 2]
                v2 = inst[p2] if m2 == 0 else p2 if m2 == 1 else inst[base + p2]

                if opt == 5:  # jump-if-true
                    ip = v2 if (v1 != 0) else ip + 3

                elif opt == 6:  # jump-if-false
                    ip = v2 if (v1 == 0) else ip + 3

                else:
                    v3 = inst[ip + 3] + (0 if m3 == 0 else base)

                    if opt == 1:  # addition
                        inst[v3] = v1 + v2

                    elif opt == 2:  # multiplication
                        inst[v3] = v1 * v2

                    elif opt == 7:  # less than
                        inst[v3] = 1 if v1 < v2 else 0

                    elif opt == 8:  # equals
                        inst[v3] = 1 if v1 == v2 else 0

                    ip += 4

        yield None


computer = Computer(list(map(int, open("13.in", "r").read().strip().split(","))))
computer.inst[0] = 2

blocks = -1
score = 0

while blocks != 0:
    blocks = 0
    command = computer.run(int(choice([0, 1, -1])))

    while True:
        x = next(command)

        if x is None:
            break

        y = next(command)
        value = next(command)

        if x == -1 and y == 0:
            if value > score:
                score = value

        elif value == 2:
            blocks += 1

print(score)
