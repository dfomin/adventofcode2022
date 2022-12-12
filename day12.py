from typing import Tuple, List


def get_neighbors(pos: Tuple[int, int], width: int, height: int) -> List[Tuple[int, int]]:
    result = []
    if pos[0] > 0:
        result.append((pos[0] - 1, pos[1]))
    if pos[0] < width - 1:
        result.append((pos[0] + 1, pos[1]))
    if pos[1] > 0:
        result.append((pos[0], pos[1] - 1))
    if pos[1] < height - 1:
        result.append((pos[0], pos[1] + 1))
    return result


def main():
    grid = []
    start = []
    end = None
    with open("inputs/day12.txt") as f:
        for row, line in enumerate(f.readlines()):
            for index, ch in enumerate(line.strip()):
                if ch in "aS":
                    start.append((index, row))
            if end is None:
                try:
                    index = line.index("E")
                    end = index, row
                except ValueError:
                    pass

            grid.append([ord(ch) - ord("a") for ch in line.strip().replace("S", "a").replace("E", "z")])

        width = len(grid[0])
        height = len(grid)

        score = [[1_000_000_000 for _ in range(width)] for _ in range(height)]
        score[end[1]][end[0]] = 0
        points_to_test = [end]
        while len(points_to_test) > 0:
            pos = points_to_test.pop(0)
            for neighbor in get_neighbors(pos, width, height):
                x, y = neighbor
                if grid[pos[1]][pos[0]] - grid[y][x] <= 1:
                    if score[y][x] > score[pos[1]][pos[0]] + 1:
                        score[y][x] = score[pos[1]][pos[0]] + 1
                        points_to_test.append((x, y))
        return min(score[y][x] for x, y in start)


if __name__ == "__main__":
    print(main())
