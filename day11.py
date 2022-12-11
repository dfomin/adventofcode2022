import operator
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional

from tqdm import tqdm


@dataclass
class Monkey:
    items: List[int]
    operation: str
    operation_param: Optional[int]
    test: int
    pass_true: int
    pass_false: int
    count: int = 0

    def send(self) -> Dict[int, List[int]]:
        self.count += len(self.items)
        result = defaultdict(list)
        for item in self.items:
            param = self.operation_param or item
            item = item + param if self.operation == "+" else item * param
            # item = item // 3
            if item % self.test == 0:
                result[self.pass_true].append(item)
            else:
                result[self.pass_false].append(item)
        self.items = []
        return result


def main():
    monkeys = []
    state = 0
    divisor = 1
    with open("inputs/day11.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue

            if state == 0:
                pass
            elif state == 1:
                items = [int(x.strip()) for x in line.split(":")[1].strip().split(",") if x]
            elif state == 2:
                first, op, second = line.split("=")[1].strip().split()

                param = None
                if second != "old":
                    param = int(second)
            elif state == 3:
                test = int(line.split()[-1])
                divisor *= test
            elif state == 4:
                pass_true = int(line.split()[-1])
            elif state == 5:
                pass_false = int(line.split()[-1])
                monkeys.append(Monkey(items, op, param, test, pass_true, pass_false))

            state = (state + 1) % 6

    for _ in tqdm(range(10_000)):
        for monkey in monkeys:
            for key, values in monkey.send().items():
                monkeys[key].items.extend([value % divisor for value in values])
    print([monkey.count for monkey in monkeys])

    s = sorted([monkey.count for monkey in monkeys])
    return s[-1] * s[-2]


if __name__ == "__main__":
    print(main())
