import time
from functools import cache

from helpers import helpers


def get_towels_and_patterns(puzzle_input):
    towels, patterns = puzzle_input.split("\n\n")
    towels = tuple(towels.split(", "))  # needs to be hashable for caching
    patterns = patterns.split("\n")
    return towels, patterns


def can_make_pattern(pattern, towels):
    if pattern in towels:
        return True
    for n in range(len(pattern)):
        if pattern[0:n] in towels:
            if can_make_pattern(pattern[n:], towels):
                return True
    return False


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    towels, patterns = get_towels_and_patterns(puzzle_input)
    return sum([1 for pattern in patterns if can_make_pattern(pattern, towels)])


@cache
def how_many_ways_can_make_pattern(pattern, towels, total=0):
    for n in range(len(pattern)):
        if pattern[0:n] in towels:
            total += how_many_ways_can_make_pattern(pattern[n:], towels)
    if pattern in towels:
        total += 1
    return total


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    towels, patterns = get_towels_and_patterns(puzzle_input)
    return sum(
        [how_many_ways_can_make_pattern(pattern, towels) for pattern in patterns]
    )


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
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
