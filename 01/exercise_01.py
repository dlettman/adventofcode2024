from collections import Counter
import re
import time

import pyperclip

from helpers import helpers

PATTERN = '([0-9]+) +([0-9]+)'


def make_lists(puzzle_input):
    l1, l2 = [], []
    for line in puzzle_input:
        nums = re.search(PATTERN, line)
        l1.append(int(nums.group(1)))
        l2.append(int(nums.group(2)))
    return l1, l2


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    l1, l2 = make_lists(puzzle_input)
    total = 0
    l1.sort()
    l2.sort()
    for zipped in zip(l1, l2):
        total += (max(zipped[0], zipped[1]) - min(zipped[0], zipped[1]))
    return total


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    l1, l2 = make_lists(puzzle_input)
    counter = Counter(l2)
    return sum([num * counter[num] for num in l1 if num in l2])


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
