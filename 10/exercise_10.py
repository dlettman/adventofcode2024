import time

import pyperclip

from helpers import helpers

from collections import deque


def convert_to_list_of_ints(pi):
    return [[int(char) for char in line] for line in pi]


def part_one(input_filename):
    grid = convert_to_list_of_ints(helpers.parse_input(input_filename))
    total = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if not char == 0:
                continue
            peaks = set()
            steps = deque([(x + n[0], y + n[1], 1) for n in helpers.NEIGHBORS_ORTH])
            while steps:
                step = steps.popleft()
                if not helpers.out_of_bounds((step[0], step[1]), grid) and grid[step[1]][step[0]] == step[2]:
                    if step[2] == 9:
                        peaks.add((step[0], step[1]))
                        continue
                    steps += ([(step[0] + n[0], step[1] + n[1], step[2] + 1) for n in helpers.NEIGHBORS_ORTH])
            total += len(peaks)
    return total


def part_two(input_filename):
    grid = convert_to_list_of_ints(helpers.parse_input(input_filename))
    big_tot = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if not char == 0:
                continue
            subtotal = 0
            steps = deque([(x + n[0], y + n[1], 1) for n in helpers.NEIGHBORS_ORTH])
            while steps:
                step = steps.popleft()
                if not helpers.out_of_bounds((step[0], step[1]), grid) and grid[step[1]][step[0]] == step[2]:
                    if step[2] == 9:
                        subtotal += 1
                        continue
                    steps += ([(step[0] + n[0], step[1] + n[1], step[2] + 1) for n in helpers.NEIGHBORS_ORTH])
            big_tot += subtotal
    return big_tot


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
