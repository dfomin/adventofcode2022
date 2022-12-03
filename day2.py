def main():
    score = 0
    optimal_score = 0
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

            if player == 2:
                optimal_score += 6 + (opponent + 1) % 3 + 1
            elif player == 1:
                optimal_score += 3 + opponent + 1
            else:
                optimal_score += (opponent - 1 + 3) % 3 + 1
    return score, optimal_score


if __name__ == "__main__":
    print(main())
