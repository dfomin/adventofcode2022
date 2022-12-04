def main():
    pairs = 0
    overlap = 0
    with open("inputs/day4.txt") as f:
        for line in f.readlines():
            ranges = [[int(x) for x in r.split("-")] for r in line.strip().split(",")]
            r1_start, r1_end = ranges[0]
            r2_start, r2_end = ranges[1]
            if r1_start <= r2_start and r1_end >= r2_end:
                pairs += 1
            elif r1_start >= r2_start and r1_end <= r2_end:
                pairs += 1

            if r1_end >= r2_start and r2_end >= r1_start:
                overlap += 1
    return pairs, overlap


if __name__ == "__main__":
    print(main())
