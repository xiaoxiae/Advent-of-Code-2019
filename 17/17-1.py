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
                inst[p1 if m1 == 0 else p1 + base] = input_value
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


class Area:
    """A class for working with the area that the robot is moving on."""

    def __init__(self):
        self.area = {}

    def __setitem__(self, i, item):
        self.area[i] = item

    def __getitem__(self, i):
        if i not in self.area:
            self.area[i] = "."

        return self.area[i]

    def get_intersections(self):
        total = 0
        for point in list(self.area.keys()):
            if area[point] == "#":
                for direction in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                    if area[(point[0] + direction[0], point[1] + direction[1])] != "#":
                        break
                else:
                    total += point[0] * point[1]

        return total


computer = Computer(list(map(int, open("17.in", "r").read().strip().split(","))))
computer.inst[0] = 2
area = Area()

x, y = 0, 0
char = computer.run(None)

# parse the map
while char != None:
    if chr(char) == "\n":
        x = 0
        y += 1
    else:
        area[(x, y)] = chr(char)
        x += 1

    char = computer.run(None)

print(area.get_intersections())
