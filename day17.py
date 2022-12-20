import time
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Rock:
    data: List[List[int]]
    x: int
    y: int

    @property
    def width(self) -> int:
        return len(self.data[0])

    @property
    def height(self) -> int:
        return len(self.data)

    def get_positions(self) -> List[Tuple[int, int]]:
        result = []
        for y, line in enumerate(self.data):
            for x, element in enumerate(line):
                if element:
                    result.append((self.x + x, self.y + y))
        return result

    def move_left(self, chamber: List[int]):
        if self.x == 0:
            return
        for y, line in enumerate(self.data):
            index = line.index(1)
            if chamber[self.y + y] & (0b1000000 >> (index + self.x - 1)):
                return
        self.x -= 1

    def move_right(self, chamber: List[int]):
        if self.x == 7 - self.width:
            return
        for y, line in enumerate(self.data):
            index = len(line) - 1 - line[::-1].index(1)
            if chamber[self.y + y] & (0b1000000 >> (index + self.x + 1)):
                return
        self.x += 1

    def move_down(self, chamber: List[int]) -> True:
        if self.y == 0:
            return True
        for y, line in enumerate(self.data):
            for x, element in enumerate(line):
                if element:
                    if chamber[self.y + y - 1] & (0b1000000 >> (self.x + x)):
                        return True
        self.y -= 1
        return False


def create_rock(index: int, height: int) -> Rock:
    if index == 0:
        return Rock([[1, 1, 1, 1]], 2, height)
    elif index == 1:
        return Rock([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]], 2, height)
    elif index == 2:
        return Rock([[1, 1, 1],
                     [0, 0, 1],
                     [0, 0, 1]], 2, height)
    elif index == 3:
        return Rock([[1],
                     [1],
                     [1],
                     [1]], 2, height)
    elif index == 4:
        return Rock([[1, 1],
                     [1, 1]], 2, height)


def chamber_pattern(chamber: List[int]) -> str:
    return "".join([str(x) for x in chamber[::-1][:100] if x > 0])


def main():
    with open("inputs/day17.txt") as f:
        pattern = f.readline()
        chamber = []
        rock_index = 0
        rock = None
        max_height = 0
        step = 0
        pattern_map = {}
        height_delta = 0
        rock_delta = 0
        finish_simulation = 1_000_000_000_001
        # finish_simulation = 2023
        calculated_height = 0
        counter = 0
        while rock_index < finish_simulation:
            if step % len(pattern) == 0:
                chp = chamber_pattern(chamber)
                if chp in pattern_map:
                    prev_rock_index, prev_height = pattern_map[chp]
                    if max_height - prev_height != height_delta:
                        pattern_map[chp] = rock_index, max_height
                        height_delta = max_height - prev_height
                        rock_delta = rock_index - prev_rock_index
                    elif counter >= 1:
                        for key in pattern_map.keys():
                            print(key)
                        calculated_height = height_delta * ((finish_simulation - rock_index) // rock_delta)
                        finish_simulation = rock_index + (finish_simulation - rock_index) % rock_delta
                        print(rock_index, rock_delta, max_height, height_delta, calculated_height, finish_simulation)
                    else:
                        pattern_map[chp] = rock_index, max_height
                        counter += 1
                else:
                    pattern_map[chp] = rock_index, max_height
            if rock is None:
                rock = create_rock(rock_index % 5, max_height + 3)
                rock_index += 1
            action = pattern[step % len(pattern)]
            if len(chamber) < max_height + 3 + rock.height:
                for _ in range(max_height + 3 + rock.height - len(chamber)):
                    chamber.append(0)
            if action == "<":
                rock.move_left(chamber)
            else:
                rock.move_right(chamber)
            if rock.move_down(chamber):
                for x, y in rock.get_positions():
                    chamber[y] |= 0b1000000 >> x
                if rock.y + rock.height > max_height:
                    max_height = rock.y + rock.height

                # if step % len(pattern) == 0:
                    # rock_positions = rock.get_positions()
                    # for y in range(len(chamber) - 1, -1, -1):
                    #     line = ""
                    #     for x in range(len(chamber[y])):
                    #         if chamber[y][x] or (x, y) in rock_positions:
                    #             line += "#"
                    #         else:
                    #             line += "."
                    #     print(line)
                    # print()

                rock = None
                # time.sleep(1)
            step += 1
        return max_height + calculated_height


if __name__ == "__main__":
    print(main())
