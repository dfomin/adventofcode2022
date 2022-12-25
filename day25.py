def snafu_to_decimal(snafu: str):
    result = 0
    for ch in snafu:
        result *= 5
        result += "=-012".index(ch) - 2
    return result


def decimal_to_snafu(value: int):
    result = ""
    while value > 0:
        value += 2
        result = f"{'=-012'[value % 5]}" + result
        value //= 5
    if len(result) == 0:
        return "="
    return result


def main():
    value = 0
    with open("inputs/day25.txt") as f:
        for line in f.readlines():
            value += snafu_to_decimal(line.strip())
    return decimal_to_snafu(value)


if __name__ == "__main__":
    print(main())
