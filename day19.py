import math
import re
from dataclasses import dataclass
from typing import Tuple, List, Optional


@dataclass
class Blueprint:
    robots: List[List[int]]


current_record = 0
visited_states = {}


@dataclass
class State:
    blueprint: Blueprint
    resources: List[int]
    robots: List[int]
    time_left: int
    _max_resource_consumption: List[int] = None

    @property
    def reward(self) -> int:
        return self.resources[-1]

    def max_resource_consumption(self) -> List[int]:
        if self._max_resource_consumption is None:
            self._max_resource_consumption = [max(robot[i] for robot in self.blueprint.robots) for i in range(len(self.robots))]
            self._max_resource_consumption[-1] = 1_000_000
        return self._max_resource_consumption

    def encode(self) -> str:
        return "".join(map(str, self.resources)) + "".join(map(str, self.robots)) + f"{self.time_left}"

    def is_enough_resources(self, required_resources: List[int]) -> bool:
        for r, rr in zip(self.resources, required_resources):
            if r < rr:
                return False
        return True

    def available_robots(self) -> List[int]:
        if self.time_left == 0:
            return []
        return [-1] + [i for i, cost in enumerate(self.blueprint.robots)
                       if self.is_enough_resources(cost) and self.robots[i] < self.max_resource_consumption()[i]]

    def build_robot(self, index: int) -> Optional['State']:
        global current_record, visited_states

        resources = [r - c * int(index >= 0) + robot
                     for r, c, robot in zip(self.resources, self.blueprint.robots[index], self.robots)]
        next_state = State(self.blueprint,
                           resources,
                           [x + int(i == index) for i, x in enumerate(self.robots)],
                           self.time_left - 1)
        if next_state.estimate_reward() < current_record:
            return None
        if next_state.encode() in visited_states and visited_states[next_state.encode()] >= self.time_left:
            return None
        visited_states[next_state.encode()] = self.time_left
        if next_state.reward > current_record:
            current_record = next_state.reward
        return next_state

    def next_states(self) -> List['State']:
        global current_record
        states = []
        for robot_id in self.available_robots():
            if state := self.build_robot(robot_id):
                states.append(state)
        return states

    def estimate_reward(self) -> int:
        return self.reward + self.robots[-1] * self.time_left + self.time_left * (self.time_left - 1) // 2


def main():
    global current_record
    global visited_states

    blueprints = []
    with open("inputs/day19.txt") as f:
        for line in f.readlines():
            groups = re.match(r".*:.*\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)", line).groups()
            blueprints.append(Blueprint([[int(groups[0]), 0, 0, 0],
                                         [int(groups[1]), 0, 0, 0],
                                         [int(groups[2]), int(groups[3]), 0, 0],
                                         [int(groups[4]), 0, int(groups[5]), 0]]))
    max_score = []
    for i, blueprint in enumerate(blueprints):
        initial_state = State(blueprint, [0] * 4, [1, 0, 0, 0], 32)
        states = [initial_state]
        while len(states) > 0:
            state = states.pop()
            states.extend(state.next_states())
        print(current_record)

        max_score.append(current_record)

        current_record = 0
        visited_states = {}

        if i == 2:
            break
    return math.prod(max_score)


if __name__ == "__main__":
    print(main())
