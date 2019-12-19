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
        self.ip = 0
        self.base = 0

    def run(self, input_value) -> Union[int, None]:
        ip = self.ip
        inst = self.inst
        base = self.base

        while inst[ip] != 99:
            opt = inst[ip] % 100

            # modes
            m1 = (inst[ip] // 100) % 10
            m2 = (inst[ip] // 1000) % 10
            m3 = (inst[ip] // 10000) % 10

            p1 = inst[ip + 1]
            v1 = inst[p1] if m1 == 0 else p1 if m1 == 1 else inst[base + p1]

            if opt == 3:  # input
                inst[p1 if m1 == 0 else p1 + base] = input_value.pop(0)
                ip += 2

            elif opt == 4:  # output
                self.ip = ip + 2
                self.base = base
                return v1

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

        return None


def get_beam_start(inst):
    """Return the proper start of the beam."""

    d = 1
    while True:
        for i in range(d):
            if Computer(inst).run([i, d]) == 1:
                return i, d
            elif Computer(inst).run([d, i]) == 1:
                return d, i

        d += 1


inst = list(map(int, open("19.in", "r").read().strip().split(",")))
R = 99  # delta of x, y

x, y = get_beam_start(inst)

while True:
    # go all the way to the right of the beam
    while Computer(inst).run([x, y]) == 1:
        x += 1

    # if the 100 x 100 box fits, print the result and exit
    if x - R - 1 >= 0 and Computer(inst).run([x - R - 1, y + R]) == 1:
        print((x - R - 1) * 10000 + y)
        exit()

    y += 1
