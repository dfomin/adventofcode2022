from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Node:
    name: str
    operation: str
    operands: List[str]
    nodes: Dict[str, 'Node']

    @property
    def eval(self) -> int:
        if self.operation == "+":
            result = self.nodes[self.operands[0]].eval + self.nodes[self.operands[1]].eval
        elif self.operation == "-":
            result = self.nodes[self.operands[0]].eval - self.nodes[self.operands[1]].eval
        elif self.operation == "*":
            result = self.nodes[self.operands[0]].eval * self.nodes[self.operands[1]].eval
        elif self.operation == "/":
            result = self.nodes[self.operands[0]].eval // self.nodes[self.operands[1]].eval
        else:
            result = int(self.operands[0])
        return result

    def seed_value(self, value: int):
        if len(self.operands) == 1:
            self.operands = [f"{value}"]
            return

        v0 = None
        v1 = None
        try:
            v0 = self.nodes[self.operands[0]].eval
        except ValueError:
            pass

        try:
            v1 = self.nodes[self.operands[1]].eval
        except ValueError:
            pass

        if v0 is None:
            if self.operation == "+":
                self.nodes[self.operands[0]].seed_value(value - v1)
            elif self.operation == "-":
                self.nodes[self.operands[0]].seed_value(value + v1)
            elif self.operation == "*":
                self.nodes[self.operands[0]].seed_value(value // v1)
            elif self.operation == "/":
                self.nodes[self.operands[0]].seed_value(value * v1)
        else:
            if self.operation == "+":
                self.nodes[self.operands[1]].seed_value(value - v0)
            elif self.operation == "-":
                self.nodes[self.operands[1]].seed_value(v0 - value)
            elif self.operation == "*":
                self.nodes[self.operands[1]].seed_value(value // v0)
            elif self.operation == "/":
                self.nodes[self.operands[1]].seed_value(v0 // value)


def main():
    nodes = {}
    with open("inputs/day21.txt") as f:
        for line in f.readlines():
            name, value = line.strip().split(": ")
            expr = value.split()
            if name == "humn":
                expr = ["none"]
            if len(expr) == 1:
                nodes[name] = Node(name, "value", [expr[0]], nodes)
            else:
                nodes[name] = Node(name, expr[1], [expr[0], expr[2]], nodes)

    try:
        value = nodes[nodes["root"].operands[0]].eval
    except ValueError:
        node = nodes[nodes["root"].operands[0]]

    try:
        value = nodes[nodes["root"].operands[1]].eval
    except ValueError:
        node = nodes[nodes["root"].operands[1]]

    node.seed_value(value)
    return nodes["humn"].eval


if __name__ == "__main__":
    print(main())
