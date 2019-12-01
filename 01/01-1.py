instructions = open("01.in", "r").read().strip().splitlines()

print(sum(map(lambda x: int(x) // 3 - 2, instructions)))
