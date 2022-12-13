from functools import cmp_to_key
from typing import List


def compare(line1: List[str], line2: List[str]) -> int:
    i = 0
    j = 0
    first_list_mode = False
    second_list_mode = False
    while i < len(line1) and j < len(line2):
        if line1[i] not in "[]" and line2[j] not in "[]":
            if int(line1[i]) == int(line2[j]):
                if first_list_mode:
                    if line2[j + 1] == "]":
                        j += 1
                    else:
                        return -1
                if second_list_mode:
                    if line1[i + 1] == "]":
                        i += 1
                    else:
                        return 1
                i += 1
                j += 1
            else:
                return -1 if int(line1[i]) < int(line2[j]) else 1
        elif line1[i] == "[" and line2[j] == "[" or line1[i] == "]" and line2[j] == "]":
            i += 1
            j += 1
        elif line1[i] == "]":
            return -1
        elif line2[j] == "]":
            return 1
        elif line1[i] == "[":
            i += 1
            second_list_mode = True
        elif line2[j] == "[":
            j += 1
            first_list_mode = True

    if i == len(line1) and j == len(line2):
        return 0
    else:
        return i == len(line1)


def main():
    with open("inputs/day13.txt") as f:
        lines_to_compare = [["[", "[", "2", "]", "]"], ["[", "[", "6", "]", "]"]]
        for line in f.readlines():
            cur_line = []
            cur_ch = ""
            for ch in line.strip():
                if ch in "0123456789":
                    cur_ch += ch
                else:
                    if len(cur_ch) > 0:
                        cur_line.append(cur_ch)
                        cur_ch = ""
                    if ch in "[]":
                        cur_line.append(ch)
            if len(cur_line) > 0:
                lines_to_compare.append(cur_line)
        sorted_list = sorted(lines_to_compare, key=cmp_to_key(compare))
        result = 1
        for i, line in enumerate(sorted_list):
            if "".join(line) == "[[2]]" or "".join(line) == "[[6]]":
                result *= i + 1
    return result


if __name__ == "__main__":
    print(main())
