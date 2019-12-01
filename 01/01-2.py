total = 0

for instruction in map(int, open("01.in", "r").read().strip().splitlines()):
    subtotal = 0
    instruction = instruction // 3 - 2

    while instruction > 0:
        subtotal += instruction
        instruction = instruction // 3 - 2

    total += subtotal

print(total)
