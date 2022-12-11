from typing import Set, List


def apply_direction():
    pass


class Rope:
    xs: List[int] = [0] * 10
    ys: List[int] = [0] * 10

    visited: Set[str] = set()

    def apply_direction(self, d: str):
        if d == "R":
            self.xs[0] += 1
        elif d == "L":
            self.xs[0] -= 1
        elif d == "U":
            self.ys[0] += 1
        elif d == "D":
            self.ys[0] -= 1

        self.check_tail(1)

    def check_tail(self, i: int):
        dx = abs(self.xs[i - 1] - self.xs[i])
        dy = abs(self.ys[i - 1] - self.ys[i])
        if dx > 1 and dy > 0 or dx > 0 and dy > 1:
            self.xs[i] += 1 if self.xs[i - 1] > self.xs[i] else -1
            self.ys[i] += 1 if self.ys[i - 1] > self.ys[i] else -1
        elif dx > 1:
            self.xs[i] += 1 if self.xs[i - 1] > self.xs[i] else -1
        elif dy > 1:
            self.ys[i] += 1 if self.ys[i - 1] > self.ys[i] else -1

        if i == len(self.xs) - 1:
            self.add_tail_position()
        else:
            self.check_tail(i + 1)

    def add_tail_position(self):
        self.visited.add(f"{self.xs[-1]}_{self.ys[-1]}")


def main():
    rope = Rope()
    with open("inputs/day9.txt") as f:
        for line in f.readlines():
            direction, steps = line.strip().split()
            for _ in range(int(steps)):
                rope.apply_direction(direction)
    return len(rope.visited)


if __name__ == "__main__":
    print(main())
