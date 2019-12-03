from typing import *


def trace_wire(instructions: List[str]) -> List[Tuple[int, int]]:
    """Return a list of (x, y) points representing the path of the wire."""
    x, y = 0, 0

    path = [(x, y)]
    for instruction in instructions:
        if instruction[0] == "R":
            x += int(instruction[1:])
        if instruction[0] == "L":
            x -= int(instruction[1:])
        if instruction[0] == "U":
            y += int(instruction[1:])
        if instruction[0] == "D":
            y -= int(instruction[1:])

        path.append((x, y))

    return path


def sign(number: int) -> int:
    """Return the signum of the number."""
    return 0 if number == 0 else -1 if number < 0 else 1


def intersections(p1s, p1e, p2s, p2e) -> Generator:
    """Generates all distances to starts of the wires for all intersections of the 
    wires."""
    x, y = p1s[0], p1s[1]

    # simulate the movement of one of the wires and check for intersections
    while (x, y) != p1e:
        if (
            x == p2s[0] == p2e[0] and min(p2s[1], p2e[1]) <= y <= max(p2s[1], p2e[1])
        ) or (
            y == p2s[1] == p2e[1] and min(p2s[0], p2e[0]) <= x <= max(p2s[0], p2e[0])
        ):
            # return the distances
            yield (
                x,
                y,
                sum([abs(p1s[0] - x), abs(p1s[1] - y)]),
                sum([abs(p2s[0] - x), abs(p2s[1] - y)]),
            )

        # move towards the end
        x += sign(p1e[0] - x)
        y += sign(p1e[1] - y)


f = open("03.in", "r").read().strip().splitlines()

p1 = trace_wire(f[0].split(","))
p2 = trace_wire(f[1].split(","))


p1_sum = 0
min_d = float("+inf")
for i in range(len(p1) - 1):
    # sum the wire along the way
    if i > 0:
        p1_sum += abs(p1[i][0] - p1[i - 1][0]) + abs(p1[i][1] - p1[i - 1][1])

    # check all pairs of segments otherwise
    p2_sum = 0
    for j in range(len(p2) - 1):
        if j > 0:
            p2_sum += abs(p2[j][0] - p2[j - 1][0]) + abs(p2[j][1] - p2[j - 1][1])

        # optimization
        if p1_sum + p2_sum > min_d:
            break

        # check for intersections
        for x, y, d1, d2 in intersections(p1[i], p1[i + 1], p2[j], p2[j + 1]):
            if (x, y) != (0, 0):
                if d1 + p1_sum + d2 + p2_sum < min_d:
                    min_d = d1 + p1_sum + d2 + p2_sum


print(min_d)
