import time

import pyperclip
from itertools import cycle
from helpers import helpers

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def parse_map(puzzle_input):
    grid = set()
    start = None
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if char == "#":
                grid.add((x, y))
            elif char == "^":
                start = tuple([x, y])
    return grid, start


def does_the_little_man_escape(grid, start, width, height):
    dirs = cycle(DIRS)
    cur_dir = next(dirs)
    cur_pos = start
    seen = {(start, cur_dir)}
    uniq_pos = {start}
    while True:
        next_pos = (cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1])
        while next_pos in grid:
            cur_dir = next(dirs)
            next_pos = (cur_pos[0] + cur_dir[0], cur_pos[1] + cur_dir[1])
        cur_pos = next_pos
        if (cur_pos, cur_dir) in seen:
            return False, len(uniq_pos)
        if not (0 <= next_pos[1] < height and 0 <= next_pos[0] < width):
            return True, len(uniq_pos)
        seen.add((cur_pos, cur_dir))
        uniq_pos.add(cur_pos)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grid, start = parse_map(puzzle_input)
    return does_the_little_man_escape(grid, start, len(puzzle_input[0]), len(puzzle_input))[1]


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grid, start = parse_map(puzzle_input)
    total = 0
    for y in range(len(puzzle_input)):
        for x in range(len(puzzle_input[0])):
            if (x, y) not in grid:
                new_grid = grid.copy()
                new_grid.add((x, y))
                if not does_the_little_man_escape(new_grid, start, len(puzzle_input[0]), len(puzzle_input[1]))[0]:
                    total += 1
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
