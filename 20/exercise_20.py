import time
from collections import deque, Counter

import pyperclip

from helpers import helpers


def get_grid(grid_input) -> (dict, tuple[int, int]):
    grid = set()
    start, end = None, None
    for y, line in enumerate(grid_input):
        for x, char in enumerate(line):
            if char == "#":
                grid.add((x, y))
            elif char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
    return grid, start, end


def print_it(width, height, walls, seen):
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) in walls:
                line += "#"
            elif (x, y) in seen:
                line += "X"
            else:
                line += "."
        print(line)


def can_get_out(start, end, width, height, walls):
    seen = {start}
    # print(seen)
    # print(walls)
    queue = deque([(start[0], start[1], 0)])  # x, y, steps
    while queue:
        move = queue.popleft()
        # print(move)
        for neighbor in helpers.NEIGHBORS_ORTH:
            new_move = (move[0] + neighbor[0], move[1] + neighbor[1], move[2] + 1)
            if (new_move[0], new_move[1]) == end:
                print_it(width, height, walls, seen)
                raise Exception
                return new_move[2]
            # print("new move = ", new_move)
            if all(
                [
                    (new_move[0], new_move[1]) not in seen,
                    0 <= new_move[0] < width,
                    0 <= new_move[1] < height,
                    (new_move[0], new_move[1]) not in walls,
                ]
            ):
                queue.append(new_move)
                seen.add((new_move[0], new_move[1]))
    return None


def get_coord_distances_from_start(start, end, width, height, walls):
    distances = {start: 0}
    seen = {start}
    queue = deque([(start[0], start[1], 0)])  # x, y, steps
    while queue:
        move = queue.popleft()
        # print(move)
        for neighbor in helpers.NEIGHBORS_ORTH:
            new_move = (move[0] + neighbor[0], move[1] + neighbor[1], move[2] + 1)
            if (new_move[0], new_move[1]) == end:
                distances[(new_move[0], new_move[1])] = new_move[2]
                print_it(width, height, walls, seen)
                return distances
            # print("new move = ", new_move)
            if all(
                [
                    (new_move[0], new_move[1]) not in seen,
                    0 <= new_move[0] < width,
                    0 <= new_move[1] < height,
                    (new_move[0], new_move[1]) not in walls,
                ]
            ):
                queue.append(new_move)
                distances[(new_move[0], new_move[1])] = new_move[2]
                seen.add((new_move[0], new_move[1]))
    return None


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    walls, start, end = get_grid(puzzle_input)
    base_escape_time = can_get_out(
        start, end, len(puzzle_input[0]), len(puzzle_input), walls
    )
    savings = Counter()
    counter = 0
    for wall in walls:
        counter += 1
        print(counter)
        if wall[0] in [0, len(puzzle_input[0]) - 1]:
            continue
        elif wall[1] in [0, len(puzzle_input) - 1]:
            continue
        these_walls = walls.copy()
        these_walls.remove(wall)
        escape_time = can_get_out(
            start, end, len(puzzle_input[0]), len(puzzle_input), these_walls
        )
        if escape_time < base_escape_time:
            savings[base_escape_time - escape_time] += 1
    return sum([v for k, v in savings.items() if k >= 100])


def manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    walls, start, end = get_grid(puzzle_input)
    distances = get_coord_distances_from_start(
        start, end, len(puzzle_input[0]), len(puzzle_input), walls
    )
    savings = Counter()
    for spot in distances:
        for other_spot in distances:
            if spot == other_spot:
                continue
            md = manhattan(spot, other_spot)
            if md <= 20:
                saving = distances[other_spot] - (distances[spot] + md)
                savings[saving] += 1
    return sum([v for k, v in savings.items() if k >= 100])


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
