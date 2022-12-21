class Node:
    def __init__(self, value: int):
        self.value = value
        self.prev = None
        self.next = None


def main():
    with open("inputs/day20.txt") as f:
        prev = None
        head = None
        nodes = []
        zero_node = None
        for value in map(int, f.readlines()):
            node = Node(value * 811589153)
            if value == 0:
                zero_node = node
            if head is None:
                head = node

            nodes.append(node)

            node.prev = prev
            if prev is not None:
                prev.next = node
            prev = node
        prev.next = head
        head.prev = prev

    for i in range(10):
        for node in nodes:
            if node.value == 0:
                continue
            forward = node.value > 0
            it = node
            node.prev.next = node.next
            node.next.prev = node.prev
            for i in range(abs(node.value) % 4999):
                if forward:
                    it = it.next
                else:
                    it = it.prev

            if not forward:
                it = it.prev

            prev_node = it
            next_node = it.next
            prev_node.next = node
            node.prev = prev_node
            next_node.prev = node
            node.next = next_node

    result = 0
    node = zero_node
    for i in range(3000):
        node = node.next
        if i % 1000 == 999:
            result += node.value
            print(node.value)
    return result


if __name__ == "__main__":
    print(main())
