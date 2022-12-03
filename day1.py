import heapq


def top1() -> int:
    current_max = 0
    current_calories = 0
    with open("inputs/day1.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                if current_calories > current_max:
                    current_max = current_calories
                current_calories = 0
            else:
                current_calories += int(line)
    return max(current_max, current_calories)


def top_n(n: int) -> int:
    heap = []
    current_calories = 0
    with open("inputs/day1.txt") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                if len(heap) < n:
                    heap.append(current_calories)
                    if len(heap) == n:
                        heapq.heapify(heap)
                elif heap[0] < current_calories:
                    heapq.heapreplace(heap, current_calories)
                current_calories = 0
            else:
                current_calories += int(line)
    return sum(heap)


if __name__ == "__main__":
    print(top_n(3))
