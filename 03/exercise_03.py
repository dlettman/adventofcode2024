import re
import time

import pyperclip

from helpers import helpers

PATTERN = "mul\\([0-9]+,[0-9]+\\)"
PATTERN2 = "mul\\(([0-9]+),([0-9]+)\\)"


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    total = 0
    for line in puzzle_input:
        matches = re.findall(PATTERN, line)
        for match in matches:
            match2 = re.search(PATTERN2, match)
            total += int(match2.group(1)) * int(match2.group(2))
    return total


def remove_dont_stuff(line, enabled=True):
    output = ""
    for idx in range(len(line)):
        try:
            if enabled and line[idx : idx + 7] == "don't()":
                enabled = False
            elif not enabled and line[idx : idx + 4] == "do()":
                enabled = True
        except IndexError:
            pass
        if enabled:
            output += line[idx]
    return output, enabled


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    total = 0
    enabled = True
    for line in puzzle_input:
        do_line, enabled = remove_dont_stuff(line, enabled=enabled)
        matches = re.findall(PATTERN, do_line)
        for match in matches:
            match2 = re.search(PATTERN2, match)
            total += int(match2.group(1)) * int(match2.group(2))
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
