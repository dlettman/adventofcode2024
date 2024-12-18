import time
from collections import deque

from helpers import helpers


def get_walls(puzzle_input):
    walls = set()
    for line in puzzle_input:
        x, y = line.split(",")
        walls.add((int(x), int(y)))
    return walls


def print_it(width, height, walls):
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) in walls:
                line += "#"
            else:
                line += "."


def can_get_out(width, height, walls):
    seen = {(0, 0)}
    queue = deque([(0, 0, 0)])  # x, y, steps
    while queue:
        move = queue.popleft()
        for neighbor in helpers.NEIGHBORS_ORTH:
            new_move = (move[0] + neighbor[0], move[1] + neighbor[1], move[2] + 1)
            if (new_move[0], new_move[1]) == (width - 1, height - 1):
                return True, new_move
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
    return False, None


def part_one(input_filename, width=71, height=71):
    puzzle_input = helpers.parse_input(input_filename)
    if len(puzzle_input) > 1024:
        puzzle_input = puzzle_input[0:1024]
    walls = get_walls(puzzle_input)
    can_escape, move = can_get_out(width, height, walls)
    if can_escape:
        return move[2]
    raise Exception("End of line, motherfucker")


def part_two(input_filename, width=71, height=71):
    puzzle_input = helpers.parse_input(input_filename)
    for n in range(1024, len(puzzle_input)):
        sub_input = puzzle_input[0:n]
        last_byte = sub_input[-1]
        walls = get_walls(sub_input)
        can_escape, move = can_get_out(width, height, walls)
        if not can_escape:
            return last_byte
    raise Exception("End of line, motherfucker")


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt', width=7, height=7)}\n")
    onestart = time.time()
    p1result = part_one("input.txt")
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    print(f"Time = {oneend - onestart}")
    print("\n")
    print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt', width=7, height=7)}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
