import time

import pyperclip

from helpers import helpers
from collections import deque

def get_region(coord, grid):
    search_queue = deque([coord])
    char = grid[coord[1]][coord[0]]
    region = set()
    region.add(coord)
    while search_queue:
        current_step = search_queue.popleft()
        for n in helpers.NEIGHBORS_ORTH:
            test_coord = (current_step[0] + n[0], current_step[1] + n[1])
            if not helpers.out_of_bounds(test_coord, grid):
                if all([not helpers.out_of_bounds(test_coord, grid),
                        grid[test_coord[1]][test_coord[0]] == char,
                        test_coord not in region]):
                    region.add(test_coord)
                    search_queue.append(test_coord)
    return region


def get_perimeter(region):
    perimeter = 0
    for coord in region:
        for n in helpers.NEIGHBORS_ORTH:
            if (coord[0] + n[0], coord[1] + n[1]) not in region:
                perimeter += 1
    return perimeter

def score_regions(regions):
    total = 0
    for region in regions:
        perimeter = get_perimeter(region)
        total += perimeter * len(region)
    return total


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    seen = set()
    regions = []
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if (x, y) not in seen:
                region = get_region((x, y), puzzle_input)
                print("region = ", region)
                seen = seen.union(region)
                regions.append(region)
    return score_regions(regions)




def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    # do stuff here
    output = None
    return output


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    onestart = time.time()
    p1result = part_one("input.txt")
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    # print(f"Time = {oneend - onestart}")
    # print("\n")
    # print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    # twostart = time.time()
    # p2result = part_two("input.txt")
    # twoend = time.time()
    # print(f"REAL RESULT = {p2result}")
    # print(f"Time = {twoend - twostart}")
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
