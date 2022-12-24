from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, List


@dataclass
class Elf:
    x: int
    y: int

    @property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y


directions = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]


def is_need_to_move(elfs: Dict[Tuple[int, int], Elf], pos: Tuple[int, int]) -> bool:
    for y in range(-1, 2):
        for x in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if (pos[0] + x, pos[1] + y) in elfs:
                return True
    return False


def is_free(elfs: Dict[Tuple[int, int], Elf], pos: Tuple[int, int], direction: Tuple[int, int]) -> bool:
    if direction[0] == 0:
        for i in range(-1, 2):
            if (pos[0] + i, pos[1] + direction[1]) in elfs:
                return False
    else:
        for i in range(-1, 2):
            if (pos[0] + direction[0], pos[1] + i) in elfs:
                return False
    return True


def print_field(elfs: Dict[Tuple[int, int], Elf]):
    min_x = min([elf.x for elf in elfs.values()])
    max_x = max([elf.x for elf in elfs.values()])
    min_y = min([elf.y for elf in elfs.values()])
    max_y = max([elf.y for elf in elfs.values()])

    field = [["." for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
    for elf in elfs.values():
        field[elf.y - min_y][elf.x - min_x] = "#"
    for line in field:
        print("".join(line))


def main():
    elfs = {}
    with open("inputs/day23.txt") as f:
        for row_id, line in enumerate(f.readlines()):
            for column_id, ch in enumerate(line.strip()):
                if ch == "#":
                    elfs[(column_id, row_id)] = Elf(column_id, row_id)

    round_id = 0
    while True:
        proposed_positions = defaultdict(list)
        for elf in elfs.values():
            if is_need_to_move(elfs, elf.pos):
                for direction_round in range(4):
                    direction = directions[(round_id + direction_round) % len(directions)]
                    if is_free(elfs, elf.pos, direction):
                        proposed_positions[(elf.pos[0] + direction[0], elf.pos[1] + direction[1])].append(elf)
                        break
        if len(proposed_positions) == 0:
            return round_id + 1
        for position, possible_elfs in proposed_positions.items():
            if len(possible_elfs) == 1:
                elf = possible_elfs[0]
                del elfs[elf.pos]
                elf.x = position[0]
                elf.y = position[1]
                elfs[elf.pos] = elf
        round_id += 1

    # min_x = min([elf.x for elf in elfs.values()])
    # max_x = max([elf.x for elf in elfs.values()])
    # min_y = min([elf.y for elf in elfs.values()])
    # max_y = max([elf.y for elf in elfs.values()])
    #
    # return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elfs)


if __name__ == "__main__":
    print(main())
