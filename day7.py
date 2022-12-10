from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Node:
    name: str
    size: int
    parent: Optional['Node']
    children: List['Node']

    def is_dir(self) -> bool:
        return len(self.children) > 0


def main():
    root = Node("/", 0, None, [])
    current = root
    with open("inputs/day7.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] == "$":
                if line == "$ cd /":
                    current = root
                elif line == "$ cd ..":
                    current = current.parent
                elif line == "$ ls":
                    pass
                else:
                    _, _, name = line.split()
                    current = [child for child in current.children if child.name == name][0]
            else:
                size, name = line.split()
                size = int(size) if size != "dir" else 0
                current.children.append(Node(name, size, current, []))
                node = current
                while node is not None:
                    node.size += size
                    node = node.parent

    s = 0
    nodes = [root]
    while len(nodes) > 0:
        node = nodes.pop(0)
        if node.size <= 100000 and node.is_dir():
            s += node.size
        nodes.extend(node.children)

    space_to_free = root.size - 40_000_000
    optimal_size = root.size
    nodes = [root]
    while len(nodes) > 0:
        node = nodes.pop(0)
        if space_to_free <= node.size < optimal_size and node.is_dir():
            optimal_size = node.size
        nodes.extend(node.children)

    return s, optimal_size


if __name__ == "__main__":
    print(main())
