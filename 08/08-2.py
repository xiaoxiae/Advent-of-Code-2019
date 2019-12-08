pixels = [int(d) for d in open("08.in", "r").read().strip()]
w, h = 25, 6

# parse the image
image = [[[] for w in range(w)] for h in range(h)]
i = 0
while i < len(pixels):
    zeroes = 0

    y = 0
    while y < h:
        x = 0
        while x < w:
            image[y][x].append(pixels[i])
            i += 1
            x += 1

        y += 1


# print out first non-transparent image in each layer
for y in range(h):
    for x in range(w):
        for p in image[y][x]:
            if p != 2:
                print("O" if p != 0 else " ", end="")
                break

    print()
