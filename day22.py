from dataclasses import dataclass, field
from typing import List, Dict, Tuple

SIZE = 50


@dataclass(repr=False)
class Node:
    x: int
    y: int
    side: int
    is_blocked: bool
    neighbors: Dict[int, 'Node'] = field(default_factory=dict)

    @property
    def row(self) -> int:
        if self.side in [0, 1]:
            return self.y
        elif self.side == 2:
            return SIZE + self.y
        elif self.side in [3, 4]:
            return 2 * SIZE + self.y
        else:
            return 3 * SIZE + self.y

    @property
    def column(self) -> int:
        if self.side in [3, 5]:
            return self.x
        elif self.side in [0, 2, 4]:
            return SIZE + self.x
        else:
            return 2 * SIZE + self.x

    def __repr__(self):
        return f"{self.x} {self.y} {self.side}"


nodes = {}
for side in range(6):
    for y in range(SIZE):
        for x in range(SIZE):
            nodes[(x, y, side)] = Node(x, y, side, False)
for side in range(6):
    for y in range(SIZE):
        for x in range(SIZE):
            if x > 0:
                nodes[(x, y, side)].neighbors[2] = nodes[(x - 1, y, side)]
            if y > 0:
                nodes[(x, y, side)].neighbors[3] = nodes[(x, y - 1, side)]
            if x < SIZE - 1:
                nodes[(x, y, side)].neighbors[0] = nodes[(x + 1, y, side)]
            if y < SIZE - 1:
                nodes[(x, y, side)].neighbors[1] = nodes[(x, y + 1, side)]


def connect_sides(sides: List[int], starts: List[Tuple[int, int]], shifts: List[Tuple[int, int]], directions: List[int]):
    for i in range(SIZE):
        nodes[(starts[0][0] + i * shifts[0][0], starts[0][1] + i * shifts[0][1], sides[0])].neighbors[directions[0]] = \
            nodes[(starts[1][0] + i * shifts[1][0], starts[1][1] + i * shifts[1][1], sides[1])]
        nodes[(starts[1][0] + i * shifts[1][0], starts[1][1] + i * shifts[1][1], sides[1])].neighbors[directions[1]] = \
            nodes[(starts[0][0] + i * shifts[0][0], starts[0][1] + i * shifts[0][1], sides[0])]


connect_sides([0, 1], [(SIZE - 1, 0), (0, 0)], [(0, 1), (0, 1)], [0, 2])
connect_sides([0, 2], [(0, SIZE - 1), (0, 0)], [(1, 0), (1, 0)], [1, 3])
connect_sides([0, 3], [(0, 0), (0, SIZE - 1)], [(0, 1), (0, -1)], [2, 2])
connect_sides([0, 5], [(0, 0), (0, 0)], [(1, 0), (0, 1)], [3, 2])

connect_sides([4, 2], [(0, 0), (0, SIZE - 1)], [(1, 0), (1, 0)], [3, 1])
connect_sides([4, 3], [(0, 0), (SIZE - 1, 0)], [(0, 1), (0, 1)], [2, 0])
connect_sides([4, 1], [(SIZE - 1, 0), (SIZE - 1, SIZE - 1)], [(0, 1), (0, -1)], [0, 0])
connect_sides([4, 5], [(0, SIZE - 1), (SIZE - 1, 0)], [(1, 0), (0, 1)], [1, 0])

connect_sides([2, 3], [(0, 0), (0, 0)], [(0, 1), (1, 0)], [2, 3])
connect_sides([3, 5], [(0, SIZE - 1), (0, 0)], [(1, 0), (1, 0)], [1, 3])
connect_sides([2, 1], [(SIZE - 1, 0), (0, SIZE - 1)], [(0, 1), (1, 0)], [0, 1])
connect_sides([1, 5], [(0, 0), (0, SIZE - 1)], [(1, 0), (1, 0)], [3, 1])


direction_change = {
    (0, 1): 0,
    (0, 2): 1,
    (0, 3): 0,
    (0, 5): 0,

    (1, 0): 2,
    (1, 2): 2,
    (1, 4): 2,
    (1, 5): 3,

    (2, 0): 3,
    (2, 1): 3,
    (2, 3): 1,
    (2, 4): 1,

    (3, 0): 0,
    (3, 2): 0,
    (3, 4): 0,
    (3, 5): 1,

    (4, 1): 2,
    (4, 2): 3,
    (4, 3): 2,
    (4, 5): 2,

    (5, 0): 1,
    (5, 1): 1,
    (5, 3): 3,
    (5, 4): 3,
}


def main():
    with open("inputs/day22.txt") as f:
        read_path = False
        for row_id, line in enumerate(f.readlines()):
            if read_path:
                path = line.strip()
            elif len(line) == 1:
                read_path = True
            else:
                for j, ch in enumerate(line.strip()):
                    if row_id < SIZE:
                        nodes[(j % SIZE, row_id, j // SIZE)].is_blocked = ch == "#"
                    elif SIZE <= row_id < 2 * SIZE:
                        nodes[(j, row_id % SIZE, 2)].is_blocked = ch == "#"
                    elif 2 * SIZE <= row_id < 3 * SIZE:
                        nodes[(j % SIZE, row_id % SIZE, j // SIZE + 3)].is_blocked = ch == "#"
                    else:
                        nodes[(j, row_id % SIZE, 5)].is_blocked = ch == "#"
    directions = "RDLU"
    direction_index = 0
    pos = nodes[(0, 0, 0)]
    i = 0
    while i < len(path):
        steps = ""
        while i < len(path) and path[i].isnumeric():
            steps += path[i]
            i += 1
        steps = int(steps)
        for j in range(steps):
            next_pos = pos.neighbors[direction_index]
            if not next_pos.is_blocked:
                if pos.side != next_pos.side:
                    direction_index = direction_change[(pos.side, next_pos.side)]
                pos = next_pos
                print(pos.x, pos.y, pos.side)
        if i < len(path):
            if path[i] == "R":
                direction_index = (direction_index + 1) % len(directions)
            else:
                direction_index = (len(directions) + direction_index - 1) % len(directions)
            i += 1
    print(1000 * (pos.row + 1) + (pos.column + 1) * 4 + direction_index)
    print(pos.x, pos.y, pos.side, direction_index)
    print(pos.row, pos.column)


if __name__ == "__main__":
    main()
