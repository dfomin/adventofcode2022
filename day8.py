def score(row, column, lines, left, right, top, bottom) -> int:
    left_value = 0
    right_value = 0
    top_value = 0
    bottom_value = 0

    i = column - 1
    while i >= 0:
        left_value += 1
        if lines[row][i] >= lines[row][column]:
            break
        i -= 1

    i = column + 1
    while i < len(lines[0]):
        right_value += 1
        if lines[row][i] >= lines[row][column]:
            break
        i += 1

    i = row - 1
    while i >= 0:
        top_value += 1
        if lines[i][column] >= lines[row][column]:
            break
        i -= 1

    i = row + 1
    while i < len(lines):
        bottom_value += 1
        if lines[i][column] >= lines[row][column]:
            break
        i += 1

    print(row, column, left_value, right_value, top_value, bottom_value)
    return left_value * right_value * top_value * bottom_value


def main():
    with open("inputs/day8.txt") as f:
        lines = [[ord(x) - ord("0") for x in line.strip()] for line in f.readlines()]
        left = [[0] * len(lines[0]) for _ in range(len(lines))]
        right = [[0] * len(lines[0]) for _ in range(len(lines))]
        top = [[0] * len(lines[0]) for _ in range(len(lines))]
        bottom = [[0] * len(lines[0]) for _ in range(len(lines))]
        for row in range(len(lines)):
            line = lines[row]
            max_left = 0
            max_right = 0
            for column in range(len(line)):
                left_value = line[column]
                left[row][column] = max_left
                max_left = max(max_left, left_value)

                right_value = line[len(line) - column - 1]
                right[row][len(line) - column - 1] = max_right
                max_right = max(max_right, right_value)

        for column in range(len(lines[0])):
            max_top = 0
            max_bottom = 0
            for row in range(len(lines)):
                top_value = lines[row][column]
                top[row][column] = max_top
                max_top = max(max_top, top_value)

                bottom_value = lines[len(lines) - 1 - row][column]
                bottom[len(lines) - 1 - row][column] = max_bottom
                max_bottom = max(max_bottom, bottom_value)

        result = 0
        best_score = 0
        for row in range(len(lines)):
            for column in range(len(line)):
                if row == 0 or row == len(lines) - 1 or column == 0 or column == len(lines[0]) - 1:
                    result += 1
                else:
                    value = lines[row][column]
                    if value > left[row][column]:
                        result += 1
                    elif value > right[row][column]:
                        result += 1
                    elif value > top[row][column]:
                        result += 1
                    elif value > bottom[row][column]:
                        result += 1

                    value = score(row, column, lines, left, right, top, bottom)
                    if value > best_score:
                        best_score = value

        return result, best_score


if __name__ == "__main__":
    print(main())
