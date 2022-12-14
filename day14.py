def main():
    with open("inputs/day14.txt") as f:
        lines = []
        for line in f.readlines():
            lines.append([[int(x) for x in point.split(",")] for point in line.strip().split(" -> ")])

        x_min = None
        x_max = None
        y_max = None
        for line in lines:
            for point in line:
                if x_min is None or x_min > point[0]:
                    x_min = point[0]
                if x_max is None or x_max < point[0]:
                    x_max = point[0]
                if y_max is None or y_max < point[1]:
                    y_max = point[1]
        y_max += 2
        x_min = min(x_min, 500 - y_max)
        x_max = max(x_max, 500 + y_max)
        area = [[0 for _ in range(x_max - x_min + 1)] for _ in range(y_max + 1)]
        for i in range(len(area[0])):
            area[y_max][i] = 1
        for line in lines:
            for i in range(1, len(line)):
                point = line[i]
                prev = line[i - 1]
                x_step = 0 if point[0] == prev[0] else 1
                y_step = 0 if point[1] == prev[1] else 1
                x = min(point[0], prev[0])
                y = min(point[1], prev[1])
                while x <= max(point[0], prev[0]) and y <= max(point[1], prev[1]):
                    area[y][x - x_min] = 1
                    x += x_step
                    y += y_step
        # for line in area:
        #     print("".join(map(str, line)))
        counter = 0
        while True:
            sand = [500 - x_min, 0]
            finish = False
            while True:
                if sand[1] == y_max:
                    finish = True
                    break
                elif area[sand[1] + 1][sand[0]] == 0:
                    sand[1] += 1
                elif sand[0] == 0:
                    area[sand[1]][sand[0]] = 2
                    finish = True
                    break
                elif area[sand[1] + 1][sand[0] - 1] == 0:
                    sand[0] -= 1
                    sand[1] += 1
                elif sand[0] == x_max - x_min:
                    finish = True
                    break
                elif area[sand[1] + 1][sand[0] + 1] == 0:
                    sand[0] += 1
                    sand[1] += 1
                else:
                    area[sand[1]][sand[0]] = 1
                    if sand[1] == 0:
                        finish = True
                    break
            counter += 1
            if finish:
                break
    for line in area:
        print("".join(map(lambda x: ".#X"[x], line)))
    print()
    return counter


if __name__ == "__main__":
    print(main())
