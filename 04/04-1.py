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

        # check for double digits
        if occurrences[digit] >= 2:
            was_digit_repeated = True

        i += 1
        number //= 10

    return was_digit_repeated


total = 0
for i in range(134792, 675811):
    if check_condition(i):
        total += 1

print(total)
