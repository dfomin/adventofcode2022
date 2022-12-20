from typing import List, Tuple


class Space:
    def __init__(self, points: List[Tuple[int, int, int]]):
        self.min_x = min(x[0] for x in points)
        self.max_x = max(x[0] for x in points)
        self.min_y = min(x[1] for x in points)
        self.max_y = max(x[1] for x in points)
        self.min_z = min(x[2] for x in points)
        self.max_z = max(x[2] for x in points)

        self.space = [
            [
                [2 for _ in range(self.max_x - self.min_x + 3)] for _ in range(self.max_y - self.min_y + 3)
            ] for _ in range(self.max_z - self.min_z + 3)
        ]

        for x, y, z in points:
            self.set_value(x, y, z, 1)

        self.mark_outside()

    def mark_outside(self):
        neighbors = [(0, 0, 0)]
        while len(neighbors) > 0:
            x, y, z = neighbors.pop()
            if self.space[z][y][x] != 2:
                continue
            self.space[z][y][x] = 0
            if x > 0:
                neighbors.append((x - 1, y, z))
            if x < len(self.space[0][0]) - 1:
                neighbors.append((x + 1, y, z))
            if y > 0:
                neighbors.append((x, y - 1, z))
            if y < len(self.space[0]) - 1:
                neighbors.append((x, y + 1, z))
            if z > 0:
                neighbors.append((x, y, z - 1))
            if z < len(self.space) - 1:
                neighbors.append((x, y, z + 1))

    def get_value(self, x: int, y: int, z: int) -> int:
        # if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y and self.min_z <= z <= self.max_z:
        #     return self.space[z - self.min_z + 1][y - self.min_y + 1][x - self.min_x + 1]
        # else:
        #     return -1
        return self.space[z - self.min_z + 1][y - self.min_y + 1][x - self.min_x + 1]

    def set_value(self, x: int, y: int, z: int, value: int):
        self.space[z - self.min_z + 1][y - self.min_y + 1][x - self.min_x + 1] = value


def main():
    with open("inputs/day18.txt") as f:
        points = []
        for line in f.readlines():
            x, y, z = map(int, line.strip().split(","))
            points.append((x, y, z))

        space = Space(points)
        result = 0

        for x, y, z in points:
            result += space.get_value(x - 1, y, z) == 0
            result += space.get_value(x + 1, y, z) == 0
            result += space.get_value(x, y - 1, z) == 0
            result += space.get_value(x, y + 1, z) == 0
            result += space.get_value(x, y, z - 1) == 0
            result += space.get_value(x, y, z + 1) == 0
        return result


if __name__ == "__main__":
    print(main())
