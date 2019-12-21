from typing import *

DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))


def change_inner_portals(area):
    explored = [[False] * len(area[0]) for _ in range(len(area))]
    stack = [(len(area[0]) // 2, len(area) // 2)]

    while len(stack) != 0:
        x, y = stack.pop(0)

        for d in DIRECTIONS:
            x_n, y_n = x + d[0], y + d[1]

            if 65 <= ord(area[y_n][x_n]) <= 90:
                area[y_n][x_n] = area[y_n][x_n].lower()

            elif area[y_n][x_n] == " " and not explored[y_n][x_n]:
                stack.append((x_n, y_n))
                explored[y_n][x_n] = True


def get_portal(area, x: int, y: int) -> Union[None, Tuple[str, Tuple[int, int]]]:
    for i, d in enumerate(DIRECTIONS):
        x_n, y_n = x + d[0], y + d[1]

        # skip if out-of-bounds
        if y_n < 0 or y_n >= len(area) or x_n < 0 or x_n >= len(area[y_n]):
            continue

        # return the tag if it's near the point (+ whether it's inner or outer)
        if 65 <= ord(area[y_n][x_n].upper()) <= 90:
            c1 = area[y_n][x_n].upper()
            c2 = area[y_n + DIRECTIONS[i][1]][x_n + DIRECTIONS[i][0]].upper()

            return "".join(sorted(c1 + c2)), (x_n, y_n), bool(ord(area[y_n][x_n]) & 32)


area = [[c for c in l] for l in open("20.in", "r").read().splitlines()]
portals = {}
start, end = None, None

# change inner portals to lower case
change_inner_portals(area)

for y in range(len(area)):
    for x in range(len(area[y])):
        if area[y][x] == ".":
            portal = get_portal(area, x, y)

            # handle portals
            if portal is not None:
                label, pos, inner = portal

                if label == "AA":
                    start = (x, y)

                elif label == "ZZ":
                    end = (x, y)

                elif label in portals:
                    p1, p2, i = portals[label]

                    area[p1[1]][p1[0]] = (x, y, i)
                    area[pos[1]][pos[0]] = (*p2, inner)
                else:
                    portals[label] = (pos, (x, y), inner)

explored = [[set() for _ in range(len(area[0]))] for _ in range(len(area))]
stack = [(*start, 0, 0)]


while len(stack) != 0:
    x, y, steps, depth = stack.pop(0)

    if (x, y) == end and depth == 0:
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

        if depth not in explored[y_n][x_n]:
            # teleport/depth change
            d = depth
            if type(area[y_n][x_n]) is tuple:
                x_n, y_n, inner = area[y_n][x_n]
                d += 1 if inner else -1

            # ignore negative depths
            if d < 0:
                continue

            stack.append((x_n, y_n, steps + 1, d))
            explored[y_n][x_n].add(d)
