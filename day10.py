def get_pixel(crt, sprite) -> str:
    if sprite <= crt <= sprite + 2:
        return "#"
    else:
        return " "


def main():
    cycle = 0
    s = 0
    next_cycle = 20
    register = 1
    result_images = []
    i = 0
    value = 0
    with open("inputs/day10.txt") as f:
        for line in f.readlines():
            line = line.strip()

            result_images.append(get_pixel(i % 40, register - 1))

            if cycle >= next_cycle:
                s += next_cycle * (register - value)
                next_cycle += 40

            if line == "noop":
                value = 0
                cycle += 1
            else:
                value = int(line.split()[1])
                register += value
                cycle += 2

                i += 1
                result_images.append(get_pixel(i % 40, register - value - 1))

            i += 1

    for i in range(6):
        print("".join(result_images[i * 40: (i + 1) * 40]))

    return s


if __name__ == "__main__":
    print(main())
