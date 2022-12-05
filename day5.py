def process_stacks(stack_lines):
    stacks = [[] for _ in range(len(stack_lines[-1].split()))]
    for line in stack_lines[-2::-1]:
        for i in range(len(stacks)):
            index = i * 4 + 1
            if line[index] != " ":
                stacks[i].append(line[index])
    return stacks


def main(keep_order):
    reading_stack = True
    stack_lines = []
    stacks = []
    with open("inputs/day5.txt") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            if reading_stack:
                if len(line) == 0:
                    reading_stack = False
                    stacks = process_stacks(stack_lines)
                else:
                    stack_lines.append(line)
            else:
                _, n, _, s, _, t = line.split()
                n = int(n)
                s = int(s) - 1
                t = int(t) - 1
                if keep_order:
                    stacks[t].extend(stacks[s][-n:])
                else:
                    stacks[t].extend(stacks[s][-1:-n - 1:-1])
                stacks[s] = stacks[s][:-n]
    return [x[-1] for x in stacks if len(x) > 0]


if __name__ == "__main__":
    print("".join(main(True)))
