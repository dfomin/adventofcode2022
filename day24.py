import heapq
from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class State:
    x: int
    y: int
    time: int
    state: int
    field: List[List[int]]
    visited_states: Dict[Tuple[int, int, int], int]
    _best_score: List[int]

    def __lt__(self, other: 'State'):
        if self.state != other.state:
            return self.state > other.state
        return self.distance_to_goal() < self.distance_to_goal()

    @property
    def finished(self) -> bool:
        if self.y == len(self.field) - 1 and self.x == len(self.field[0]) - 2 and self.state != 1:
            if self.time < self.best_score:
                self._best_score[0] = self.time
            return True
        elif self.y == 0 and self.x == 1 and self.state == 1:
            if self.time < self.best_score:
                self._best_score[0] = self.time
            return True
        return False

    @property
    def best_score(self) -> int:
        return self._best_score[0]

    @property
    def promising(self) -> bool:
        if self.y < 0 or self.y >= len(self.field):
            return False
        if self.field[self.y][self.x] == 5:
            return False
        width = len(self.field[0]) - 2
        height = len(self.field) - 2
        if self.field[self.y][(self.x - 1 + width - self.time % width) % width + 1] == 0:
            return False
        if self.field[(self.y - 1 + height - self.time % height) % height + 1][self.x] == 1:
            return False
        if self.field[self.y][(self.x - 1 + self.time % width + width) % width + 1] == 2:
            return False
        if self.field[(self.y - 1 + self.time % height + height) % height + 1][self.x] == 3:
            return False
        if self.time >= self.best_score:
            return False
        if (self.x, self.y, self.time % (width * height)) in self.visited_states:
            if self.visited_states[(self.x, self.y, self.time % (width * height))] <= self.time:
                return False
        return True

    def distance_to_goal(self) -> int:
        if self.state == 1:
            return self.x + self.y
        else:
            return len(self.field) - self.y + len(self.field[0]) - self.x

    def next_states(self) -> List['State']:
        next_states = []
        for dx, dy in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_state = State(self.x + dx, self.y + dy, self.time + 1, self.state, self.field, self.visited_states, self._best_score)
            if next_state.finished:
                continue
            elif next_state.promising:
                next_states.append(next_state)
                width = len(self.field[0]) - 2
                height = len(self.field) - 2
                self.visited_states[(next_state.x, next_state.y, next_state.time % (width * height))] = next_state.time
        return next_states


def calculate_time(field: List[List[int]], x: int, y: int, time: int, state: int):
    initial_state = State(x, y, time, state, field, {}, [1_000_000_000])
    states = [initial_state]
    while len(states) > 0:
        # state = heapq.heappop(states)
        state = states.pop(0)
        states.extend(state.next_states())
        # heapq.heappush(states, s)
    return initial_state.best_score


def main():
    field = []
    with open("inputs/day24.txt") as f:
        for line in f.readlines():
            row = []
            for ch in line.strip():
                if ch == ".":
                    row.append(4)
                elif ch == "#":
                    row.append(5)
                else:
                    row.append(">v<^".index(ch))
            field.append(row)

    t1 = calculate_time(field, 1, 0, 0, 0)
    print(t1)
    t2 = calculate_time(field, len(field[0]) - 2, len(field) - 1, t1, 1)
    print(t2)
    t3 = calculate_time(field, 1, 0, t2, 2)
    return t3


if __name__ == "__main__":
    print(main())
