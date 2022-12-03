CHAR_DICT = {chr(x + ord("a")): x for x in range(26)} | {chr(x + ord("A")): x + 26 for x in range(26)}


def main():
    with open("inputs/day3.txt") as f:
        wrong_sum = 0
        badge_sum = 0
        rucksack_index = 1
        for line in f.readlines():
            line = line.strip()
            letter_stats = [0] * len(CHAR_DICT)
            if rucksack_index == 1:
                common_stats = [0] * len(CHAR_DICT)
            wrong_index = None
            badge_index = None
            for i, ch in enumerate(line):
                ch_index = CHAR_DICT[ch]
                if wrong_index is None:
                    if i < len(line) // 2:
                        letter_stats[ch_index] = 1
                    else:
                        if letter_stats[ch_index] > 0:
                            wrong_index = ch_index + 1
                if badge_index is None:
                    if common_stats[ch_index] == rucksack_index - 1:
                        if rucksack_index == 3:
                            badge_index = ch_index + 1
                        else:
                            common_stats[ch_index] = rucksack_index
            wrong_sum += wrong_index
            badge_sum += badge_index if badge_index is not None else 0

            rucksack_index = rucksack_index % 3 + 1
        return wrong_sum, badge_sum


if __name__ == "__main__":
    print(main())
