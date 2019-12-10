from math import gcd, atan2, pi


def in_sight(x1, y1, x2, y2, area):
    """Returns True if asteroid at x2, y2 is in sight of the one at x1, y1."""
    # skip itself
    if x1 == x2 and y1 == y2:
        return False

    # go to the coordinate
    x_d, y_d = x2 - x1, y2 - y1
    multiple = gcd(x_d, y_d)

    x_step, y_step = x_d // multiple, y_d // multiple

    x1 += x_step
    y1 += y_step

    # jump to x2, y2 until we hit something
    while x1 != x2 or y1 != y2:
        if area[y1][x1] == "#":
            return False

        x1 += x_step
        y1 += y_step

    # if we didn't hit something, the position is valid!
    return True


area = open("10.in", "r").read().strip().splitlines()

max_sight = 0
x, y = 0, 0  # station x, y

for y1 in range(len(area)):
    for x1 in range(len(area[0])):
        subtotal = 0

        if area[y1][x1] == "#":
            for y2 in range(len(area)):
                for x2 in range(len(area[0])):
                    if area[y2][x2] == "#" and in_sight(x1, y1, x2, y2, area):
                        subtotal += 1

            if max_sight < subtotal:
                max_sight = subtotal
                x, y = x1, y1


# get the coordinates of all asteroids
asteroids = []
for y1 in range(len(area)):
    for x1 in range(len(area[0])):
        if area[y1][x1] == "#":
            asteroids.append((x1, y1))

# sort their positions on their angles with the base station
asteroids.sort(key=lambda c: (atan2(y - c[1], x - c[0]) + pi / 2) % pi * 2)
asteroids_to_remove = []
removed_asteroids = 0

while len(asteroids) != 0:
    for asteroid in asteroids:
        # mark each asteroid in sight to be removed
        if in_sight(x, y, asteroid[0], asteroid[1], area):
            asteroids_to_remove.append(asteroid)
            removed_asteroids += 1

            # if we're on the 200th, hooray!
            if removed_asteroids == 200:
                print(asteroid[0] * 100 + asteroid[1])
                exit()

    # remove marked asteroids
    while len(asteroids_to_remove) != 0:
        asteroids.remove(asteroids_to_remove.pop())

print("Not enough asteroids!")
