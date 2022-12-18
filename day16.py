import itertools
import re
from dataclasses import dataclass
from functools import lru_cache
from time import time
from typing import List, Dict, Tuple, Optional

from tqdm import tqdm


@dataclass
class Node:
    name: str
    rate: int
    connections: List[str]


@dataclass
class State:
    name: str
    valves: List[int]
    score: int
    time_left: int
    nodes: Dict[str, Node]
    visited_states: Dict[str, List[int]]
    current_max_score: List[int]
    parent: Optional['State']
    dist: List[List[int]]

    @property
    def max_score(self) -> int:
        return self.current_max_score[0]

    def encode(self) -> str:
        return f"{self.name}_{''.join([str(x) for x in self.valves])}"

    def estimate_max_score(self) -> int:
        closed_valves = sorted([node.rate for i, node in enumerate(self.nodes.values()) if self.valves[i] == 0],
                               reverse=True)
        score = self.score
        time_left = self.time_left
        i = 0
        while i < len(closed_valves):
            rate = closed_valves[i]
            score += time_left * rate
            time_left -= 2
            if time_left <= 0:
                break
            i += 1
        return score

    def apply_actions(self, action: str) -> Optional['State']:
        valves = self.valves.copy()
        score = self.score

        source_index = list(self.nodes.keys()).index(self.name)
        target_index = list(self.nodes.keys()).index(action)
        time_left = self.time_left
        if self.name == action and valves[source_index] == 0:
            time_left -= 1
            valves[source_index] = 1
            score += time_left * self.nodes[self.name].rate
            if score > self.max_score:
                self.current_max_score[0] = score
                # path = f"{action}"
                # node = self.parent
                # while node is not None:
                #     path = f"{node.name} -> {path}"
                #     node = node.parent
                # print(self.max_score, path)
        else:
            time_left -= self.dist[source_index][target_index]

        return State(action,
                     valves,
                     score,
                     time_left,
                     self.nodes,
                     self.visited_states,
                     self.current_max_score,
                     self,
                     self.dist)

    def generate_next_states(self) -> List['State']:
        if self.time_left <= 0:
            return []
        result = []
        for action in self.possible_actions():
            next_state = self.apply_actions(action)
            if next_state is None:
                continue
            encoded_next_state = next_state.encode()
            if encoded_next_state in self.visited_states:
                cached_values = self.visited_states[encoded_next_state]
                values = [next_state.time_left, next_state.score]
                skip = True
                for cached_value, value in zip(cached_values, values):
                    if cached_value < value:
                        skip = False
                        break
                if skip:
                    continue
            if next_state.estimate_max_score() < self.max_score:
                continue
            self.visited_states[encoded_next_state] = [next_state.time_left, next_state.score]
            result.append(next_state)
        return result

    def possible_actions(self) -> List[str]:
        actions = []
        if self.valves[list(self.nodes.keys()).index(self.name)] == 0:
            actions.append(self.name)
        actions.extend([x for i, x in enumerate(list(self.nodes.keys())) if self.valves[i] == 0 and self.name != x])
        return actions


def main():
    nodes = {}
    with open("inputs/day16.txt") as f:
        for i, line in enumerate(f.readlines()):
            pattern = re.compile(r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")
            name, rate, connections = pattern.match(line.strip()).groups()
            nodes[name] = Node(name, int(rate), connections.split(", "))
    graph = [[1_000_000 for _ in range(len(nodes))] for _ in range(len(nodes))]
    for i in range(len(graph)):
        graph[i][i] = 0
    for i, node in enumerate(nodes.values()):
        for connection in node.connections:
            graph[i][list(nodes.keys()).index(connection)] = 1
    for k in range(len(nodes)):
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if graph[i][j] > graph[i][k] + graph[k][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]
    broken_valves = [i for i in range(len(list(nodes.values())))
                     if list(nodes.values())[i].rate == 0 and list(nodes.values())[i].name != "AA"]
    nodes = {name: node for i, (name, node) in enumerate(nodes.items()) if i not in broken_valves}
    dist = []
    for i in range(len(graph)):
        if i in broken_valves:
            continue
        dist.append([graph[i][j] for j in range(len(graph[i])) if j not in broken_valves])

    max_score = 0
    for i in tqdm(range(len(nodes) // 2 + 1)):
        for mine in itertools.combinations(range(len(nodes)), i):
            my_valves = [int(i in mine) for i in range(len(nodes))]
            elephant_valves = [int(i not in mine) for i in range(len(nodes))]
            my_valves[list(nodes.keys()).index("AA")] = 1
            elephant_valves[list(nodes.keys()).index("AA")] = 1
            my_state = State("AA", my_valves, 0, 26, nodes, {}, [0], None, dist)
            elephant_state = State("AA", elephant_valves, 0, 26, nodes, {}, [0], None, dist)

            for initial_state in [my_state, elephant_state]:
                next_states = initial_state.generate_next_states()
                while len(next_states) > 0:
                    next_state = next_states.pop()
                    next_states.extend(next_state.generate_next_states())

            if my_state.max_score + elephant_state.max_score > max_score:
                max_score = my_state.max_score + elephant_state.max_score
                print(max_score)
    # initial_state = State("AA", valves, 0, 30, nodes, {}, [0], None, dist)
    # next_states = initial_state.generate_next_states()
    # while len(next_states) > 0:
    #     next_state = next_states.pop()
    #     next_states.extend(next_state.generate_next_states())
    return max_score


if __name__ == "__main__":
    start = time()
    print(main())
    print(time() - start)
