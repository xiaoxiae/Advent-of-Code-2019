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


class Area:
    """A class for working with the area that the robot is moving on."""

    orientation = {">": 0, "^": 1, "<": 2, "v": 3}
    directions = ((1, 0), (0, -1), (-1, 0), (0, 1))

    def __init__(self):
        self.area = {}

    def __setitem__(self, i, item):
        self.area[i] = item

    def __getitem__(self, i):
        if i not in self.area:
            self.area[i] = "."

        return self.area[i]

    def __get_next_direction(self, x, y, visited):
        """Get the direction of the next move for a given path."""
        for i, direction in enumerate(self.directions):
            point = (x + direction[0], y + direction[1])
            if point not in visited and area[point] == "#":
                return i

    def get_path(self):
        """Return the shortest path (commands) that visits each point at least once."""
        # get the robot position
        robot_position = None
        robot_orientation = None

        for point in self.area:
            if self[point] in self.orientation:
                robot_position = point
                robot_orientation = self.orientation[self[point]]
                break

        visited = set([point])  # the set of visited points
        path = []

        x, y = point
        while True:
            o = self.__get_next_direction(x, y, visited)

            # if there is nowhere to go, terminate
            if o == None:
                break

            # adjust the robot orientation
            turn_delta = robot_orientation - o
            turn_delta += -4 if turn_delta >= 3 else 4 if turn_delta <= -3 else 0
            path.append("L" * abs(turn_delta) if turn_delta < 0 else "R" * turn_delta)
            robot_orientation = o

            # move as much as we can in the given direction
            move_length = 0
            while area[(x + self.directions[o][0], y + self.directions[o][1])] != ".":
                move_length += 1

                x += self.directions[o][0]
                y += self.directions[o][1]

                visited.add((x, y))

            path.append(move_length)

        return path


def get_replacements(path):
    """Generate possible replacements of the path, returning the replacement and
    whatever is left of the path."""
    # check all possible starts
    for i in range(2, 11):
        p = [c for c in path]
        r = path[:i]

        j = 0
        while j <= len(p) - len(r):
            if p[j : j + len(r)] == r:
                p = p[:j] + p[j + len(r) :]
            else:
                j += 1

        yield p, r


def get_instructions(path):
    """Get the sequence of instructions to feed to the computer."""
    for p, r1 in get_replacements(path):
        for p, r2 in get_replacements(p):
            for p, r3 in get_replacements(p):
                if len(p) == 0:
                    registers = (r1, r2, r3)

                    i = 0
                    while i != len(path):
                        for j, r in enumerate(registers):
                            if path[i : i + len(r)] == r:
                                path = (
                                    path[:i] + [chr(ord("A") + j)] + path[i + len(r) :]
                                )
                        i += 1

                    instructions = []

                    for piece in [path, r1, r2, r3]:
                        for char in ",".join(list(map(str, piece))):
                            instructions.append(ord(char))
                        instructions.append(10)

                    instructions.append(ord("n"))
                    instructions.append(10)

                    return instructions


inst = list(map(int, open("17.in", "r").read().strip().split(",")))
computer = Computer([i for i in inst])
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

computer = Computer(inst)
computer.inst[0] = 2

# load the instructions to the computer
instructions = get_instructions(area.get_path())
while len(instructions) != 0:
    computer.run(instructions)

# run the program
prev_out = None
out = computer.run(None)
while out is not None:
    prev_out = out
    out = computer.run(None)

print(prev_out)
