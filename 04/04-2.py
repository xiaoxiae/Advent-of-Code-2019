def check_condition(number: int) -> str:
    """Checks, whether the number satisfies the condition."""
    occurrences = [0] * 10
    was_digit_repeated = False
    previous_digit = 10

    i = 0
    while number != 0:
        digit = number % 10

        # check for ascending digit
        if previous_digit < digit:
            return False

        previous_digit = digit
        occurrences[digit] += 1

        i += 1
        number //= 10

    # check for a group of exactly 2 digits
    for occurrence in occurrences:
        if occurrence == 2:
            was_digit_repeated = True

    return was_digit_repeated


total = 0
for i in range(*map(int, open("04.in", "r").read().strip().split(","))):
    if check_condition(i):
        total += 1

print(total)
