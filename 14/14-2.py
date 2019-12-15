from __future__ import annotations
from typing import *
from dataclasses import dataclass
from collections import defaultdict

from math import ceil


def parse_value(value: str) -> Tuple[str, int]:
    a, b = value.strip().split(" ")
    return b, int(a)


@dataclass
class Resource:
    quantity: int
    requires: List[Tuple[str, int]]


resources: Dict[str, Resource] = {}
byproducts = defaultdict(lambda: 0)  # for storing leftover chemicals

for line in open("14.in", "r").read().strip().splitlines():
    l, r = line.split(" => ")

    chemical, quantity = parse_value(r)
    resources[chemical] = Resource(quantity, [])

    for value in map(parse_value, l.split(", ")):
        resources[chemical].requires.append(value)


def get_cost(chemical, quantity):
    """Recursively retrieve the cost of a chemical."""
    resource = resources[chemical]

    # calculate the minimum allowed quantity + the leftovers
    quantity_coefficient = ceil(quantity / resource.quantity)
    byproducts[chemical] += quantity_coefficient * resource.quantity - quantity

    # base condition -- ores
    if resource.requires[0][0] == "ORE":
        return resource.requires[0][1] * quantity_coefficient

    cost = 0
    for r_chemical, r_quantity in resource.requires:
        # make use of the byproducts
        if byproducts[r_chemical] >= r_quantity * quantity_coefficient:
            byproducts[r_chemical] -= r_quantity * quantity_coefficient
        else:
            r_quantity = r_quantity * quantity_coefficient - byproducts[r_chemical]
            byproducts[r_chemical] = 0

            cost += get_cost(r_chemical, r_quantity)

    return cost


# binary search for the correct amount of fuel
input_size = 1000000000000
lo, hi = 0, input_size

while lo < hi:
    avg = (lo + hi) // 2

    if get_cost("FUEL", avg) < input_size:
        lo = avg + 1
    else:
        hi = avg

print(lo - 1)
