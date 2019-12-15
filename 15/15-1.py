from random import *
from typing import *

from time import sleep


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

    def run(self, input_value) -> Union[int, None]:
        """"""
        ip = self.ip
        inst = self.inst

        base = 0
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
            self.area[i] = " "

        return self.area[i]

    def paint(self):
        """Paints the area that the robot drew on."""
        coordinates = list(self.area)

        min_x = min(coordinates)[0]
        min_y = min(coordinates, key=lambda x: x[1])[1]

        max_x = max(coordinates)[0]
        max_y = max(coordinates, key=lambda x: x[1])[1]

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                print(self[(x, y)], end="")
            print()


computer = Computer(list(map(int, open("15.in", "r").read().strip().split(","))))
area = Area()
area[(0, 0)] = "."

directions = [(), (0, 1), (0, -1), (-1, 0), (1, 0)]
stack: List[List[int]] = [[]]

while len(stack) != 0:
    moves = stack.pop()
    x, y = 0, 0

    # get to the end spot
    for move in moves:
        computer.run(move)
        x += directions[move][0]
        y += directions[move][1]

    # run the robot in each of the 4 directions
    for d in range(1, 5):
        x_n, y_n = x + directions[d][0], y + directions[d][1]

        # if we've been here, simply continue
        if area[(x_n, y_n)] != " ":
            continue

        status = computer.run(d)

        if status == 0:
            area[(x_n, y_n)] = "#"

        elif status == 1:
            area[(x_n, y_n)] = "."
            stack.append([m for m in moves] + [d])
            computer.run(1 if d == 2 else 2 if d == 1 else 4 if d == 3 else 3)

        else:
            print(len(moves) + 1)
            exit()

    # get back to the beginning
    for move in reversed(moves):
        computer.run(1 if move == 2 else 2 if move == 1 else 4 if move == 3 else 3)
