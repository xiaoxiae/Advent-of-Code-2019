from typing import Dict, List


orbits = open("06.in", "r").read().strip().splitlines()
tree: Dict[str, List] = {}

# create a two-way tree
for orbit in orbits:
    v1, v2 = orbit.split(")")

    if v1 not in tree:
        tree[v1] = [v2]
    else:
        tree[v1].append(v2)

    if v2 not in tree:
        tree[v2] = [v1]
    else:
        tree[v2].append(v1)

# bfs variables
stack = [("YOU", 0)]
visited = set()

# run bfs
while len(stack) != 0:
    current, value = stack.pop()
    visited.add(current)

    if current == "SAN":
        print(value - 2)
        break

    else:
        if current in tree:
            stack += [(v, value + 1) for v in tree[current] if v not in visited]
