def main():
    current_max = 0
    current_calories = 0
    with open("inputs/day1.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                if current_calories > current_max:
                    current_max = current_calories
                current_calories = 0
            else:
                current_calories += int(line)
    print(max(current_max, current_calories))


if __name__ == "__main__":
    main()
