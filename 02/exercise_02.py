import time

import pyperclip

from helpers import helpers


def is_ok(line, mini=False):
    safe = True
    if not sorted(line) == line and not sorted(line) == line[::-1]:
        safe = False
    if safe:
        line_c = sorted(line)
        prev_num = line_c[0]
        for num in line_c[1:]:
            if not (prev_num + 3) >= num > prev_num:
                safe = False
                break
            prev_num = num
    if not mini and not safe:
        sub_seqs = []
        for n in range(1, len(line) + 1):
            sub_seqs.append(line[0 : n - 1] + line[n : len(line)])
        return any([is_ok(sub_seq, mini=True) for sub_seq in sub_seqs])
    return safe


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    reports = [[int(item) for item in line.split()] for line in puzzle_input]
    return sum([1 for report in reports if is_ok(report, mini=True)])


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    reports = [[int(item) for item in line.split()] for line in puzzle_input]
    total = sum([1 for report in reports if is_ok(report)])
    return total


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    onestart = time.time()
    p1result = part_one("input.txt")
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    print(f"Time = {oneend - onestart}")
    print("\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
