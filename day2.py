def main():
    score = 0
    with open("inputs/day2.txt") as f:
        for line in f.readlines():
            opponent, player = line.strip().split(" ")
            opponent = ord(opponent) - ord("A")
            player = ord(player) - ord("X")
            if player == opponent:
                score += 3
            elif (player - opponent + 3) % 3 == 1:
                score += 6
            score += player + 1
    return score


if __name__ == "__main__":
    print(main())
