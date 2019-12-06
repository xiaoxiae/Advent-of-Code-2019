from typing import Dict, List


orbits = open("06.in", "r").read().strip().splitlines()
tree: Dict[str, List] = {}

# create a one-way tree
for orbit in orbits:
    v1, v2 = orbit.split(")")

    if v1 not in tree:
        tree[v1] = [v2]
    else:
        tree[v1].append(v2)


def dfs(v1, depth) -> int:
    """A depth-first search for the sum of depths from the root."""
    return depth + (sum(dfs(v, depth + 1) for v in tree[v1]) if v1 in tree else 0)


print(dfs("COM", 0))
