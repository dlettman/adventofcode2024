import time
import pyperclip
from itertools import combinations

import helpers


def parse_map(puzzle_input):
    antennas = {}
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if char != ".":
                if char in antennas:
                    antennas[char].add((x, y))
                else:
                    antennas[char] = {(x, y)}
    return antennas


def print_the_thing(antinodes, puzzle_input):
    for y in range(len(puzzle_input)):
        line = ""
        for x in range(len(puzzle_input[0])):
            if (x, y) in antinodes:
                line += "#"
            else:
                line += "."
        print(line)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    antinodes = set()
    antennas = parse_map(puzzle_input)
    for char, char_antennas in antennas.items():
        for antenna, other_antenna in combinations(char_antennas, 2):
            dist = (antenna[0] - other_antenna[0], antenna[1] - other_antenna[1])
            loc = (antenna[0] + dist[0], antenna[1] + dist[1])
            if not helpers.out_of_bounds(loc, puzzle_input):
                antinodes.add(loc)
            loc = (other_antenna[0] - dist[0], other_antenna[1] - dist[1])
            if not helpers.out_of_bounds(loc, puzzle_input):
                antinodes.add(loc)
    return len(antinodes)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    antinodes = set()
    antennas = parse_map(puzzle_input)
    for char, char_antennas in antennas.items():
        for antenna, other_antenna in combinations(char_antennas, 2):
            dist = (antenna[0] - other_antenna[0], antenna[1] - other_antenna[1])
            loc = antenna
            while not helpers.out_of_bounds(loc, puzzle_input):
                antinodes.add(loc)
                loc = (loc[0] + dist[0], loc[1] + dist[1])
            loc = other_antenna
            while not helpers.out_of_bounds(loc, puzzle_input):
                antinodes.add(loc)
                loc = (loc[0] - dist[0], loc[1] - dist[1])
    return len(antinodes)


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
