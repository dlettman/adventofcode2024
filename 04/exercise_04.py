import time

import pyperclip

from helpers import helpers


DIAG_PAIRS = [((1, 1), (-1, -1)), ((1, -1), (-1, 1))]


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    total = 0
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if not char == "X":
                continue
            for x_delta, y_delta in helpers.NEIGHBORS:
                xmas = True
                for dist, letter in [(1, "M"), (2, "A"), (3, "S")]:
                    y_coord, x_coord = y + y_delta * dist, x + x_delta * dist
                    if helpers.out_of_bounds((x_coord, y_coord), puzzle_input) or (
                        not puzzle_input[y_coord][x_coord] == letter
                    ):
                        xmas = False
                        break
                if xmas:
                    total += 1
    return total


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    total = 0
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if not char == "A":
                continue
            xmas = True
            for delta_a, delta_b in DIAG_PAIRS:
                if any(
                    [
                        helpers.out_of_bounds(
                            (x + delta_a[0], y + delta_a[1]), puzzle_input
                        ),
                        helpers.out_of_bounds(
                            ((x + delta_b[0]), y + delta_b[1]), puzzle_input
                        ),
                    ]
                ):
                    xmas = False
                    break
                coord_one, coord_two = (x + delta_a[0], y + delta_a[1]), (
                    x + delta_b[0],
                    y + delta_b[1],
                )
                if not (
                    (
                        puzzle_input[coord_one[1]][coord_one[0]] == "M"
                        and puzzle_input[coord_two[1]][coord_two[0]] == "S"
                    )
                    or (
                        puzzle_input[coord_one[1]][coord_one[0]] == "S"
                        and puzzle_input[coord_two[1]][coord_two[0]] == "M"
                    )
                ):
                    xmas = False
                    break
            if xmas:
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
