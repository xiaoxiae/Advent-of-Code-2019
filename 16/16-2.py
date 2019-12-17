from typing import *


def get_prefix_sum(s: int, e: int, prefixes: List[int]):
    """Calculate the sum of a segment [s, e]."""
    # restrict start and end
    s = max(0, s)
    e = min(len(prefixes) - 1, e)

    return prefixes[e] - (0 if s - 1 < 0 else prefixes[s - 1])


input_list = list(map(int, str(open("16.in", "r").read().strip()))) * 10000
pattern = [0, 1, 0, -1]
delta = 1

start = time()

prefixes = [0] * len(input_list)
output_list = [0] * len(input_list)

pos = int("".join(list(map(str, input_list[:7]))))

for n in range(100):
    # calculate prefix sums and zero the output list
    total = 0
    for i in range(len(prefixes)):
        total += input_list[i]
        prefixes[i] = total
        output_list[i] = 0

    for i in range(len(input_list)):
        index = delta // (i + 1)  # index in pattern
        j = -delta  # starting position in the list

        while j < len(input_list):
            s, e = j, j + i

            # ignore nonsensical values
            if s >= 0 or e >= 0:
                prefix_sum = get_prefix_sum(s, e, prefixes)
                output_list[i] += prefix_sum * pattern[index % len(pattern)]
                index += 1

            j += i + 1

        output_list[i] = abs(output_list[i]) % 10

    input_list, output_list = output_list, input_list

print("".join(list(map(str, input_list[pos : pos + 8]))))
