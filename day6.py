def main(length: int):
    with open("inputs/day6.txt") as f:
        line = f.readline().strip()
        start_unique = 0
        end_unique = 0
        while end_unique - start_unique < length - 1:
            end_unique += 1
            i = end_unique - 1
            while i >= start_unique and line[end_unique] != line[i]:
                i -= 1
            start_unique = i + 1
        return end_unique + 1


if __name__ == "__main__":
    print(main(14))
