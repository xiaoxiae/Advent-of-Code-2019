from typing import *

DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))


def get_portal(area, x: int, y: int) -> Union[None, Tuple[str, Tuple[int, int]]]:
    """Return the tag of the portal at the dot, or None if there isn't one."""

    for i, d in enumerate(DIRECTIONS):
        x_n, y_n = x + d[0], y + d[1]

        # skip if out-of-bounds
        if y_n < 0 or y_n >= len(area) or x_n < 0 or x_n >= len(area[y_n]):
            continue

        # return the tag if it's near the point
        if 65 <= ord(area[y_n][x_n]) <= 90:
            c1 = area[y_n][x_n]
            c2 = area[y_n + DIRECTIONS[i][1]][x_n + DIRECTIONS[i][0]]

            return "".join(sorted(c1 + c2)), (x_n, y_n)


area = [[c for c in l] for l in open("20.in", "r").read().splitlines()]
portals = {}
start, end = None, None

for y in range(len(area)):
    for x in range(len(area[y])):
        if area[y][x] == ".":
            portal = get_portal(area, x, y)

            # handle portals
            if portal is not None:
                label, pos = portal

                if label == "AA":
                    start = (x, y)

                elif label == "ZZ":
                    end = (x, y)

                elif label in portals:
                    p1, p2 = portals[label]

                    area[p1[1]][p1[0]] = (x, y)
                    area[pos[1]][pos[0]] = p2
                else:
                    portals[label] = (pos, (x, y))

explored = [[False] * len(area[0]) for _ in range(len(area))]
stack = [(*start, 0)]

while len(stack) != 0:
    x, y, steps = stack.pop(0)
    explored[y][x] = True

    if (x, y) == end:
        print(steps)
        exit()

    for d in DIRECTIONS:
        x_n, y_n = x + d[0], y + d[1]

        # skip if out-of-bounds
        if y_n < 0 or y_n >= len(area) or x_n < 0 or x_n >= len(area[y_n]):
            continue

        # skip non-walkable spaces
        if area[y_n][x_n] != "." and not (type(area[y_n][x_n]) is tuple):
            continue

        # transform coordinates with portals
        if type(area[y_n][x_n]) is tuple:
            x_n, y_n = area[y_n][x_n]

        if not explored[y_n][x_n]:
            stack.append((x_n, y_n, steps + 1))
