pixels = [int(d) for d in open("08.in", "r").read().strip()]

w, h = 25, 6

min_zeroes = float("+inf")
min_zeroes_value = 0

# count occurrences layer by layer
for i in range(0, len(pixels), w * h):
    layer = pixels[i : i + w * h]

    if layer.count(0) < min_zeroes:
        min_zeroes_value = layer.count(1) * layer.count(2)
        min_zeroes = layer.count(0)

print(min_zeroes_value)
