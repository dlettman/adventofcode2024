import time
from copy import deepcopy

from helpers import helpers


def get_grid(grid_input) -> (dict, tuple[int, int]):
    grid = {}
    robot = None
    for y, line in enumerate(grid_input.split("\n")):
        for x, char in enumerate(line):
            if char in "#O":
                grid[(x, y)] = char
            if char == "@":
                robot = (x, y)
    return grid, robot


MOVES_MAP = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


def get_moves(moves_input) -> list:
    print(moves_input, type(moves_input))
    moves_input = "".join(moves_input.split("\n"))
    return [MOVES_MAP[dir] for dir in moves_input]


def push_box(
    grid: dict, coord: tuple, direction: tuple, incoming_box=False
) -> (bool, dict):
    current_coord = coord
    while True:
        next_coord = (current_coord[0] + direction[0], current_coord[1] + direction[1])
        if next_coord not in grid:
            grid[next_coord] = "O"
            if not incoming_box:
                del grid[current_coord]
            return True, grid
        elif grid[next_coord] == "#":
            return False, grid
        elif grid[next_coord] == "O":
            can_push, grid = push_box(grid, next_coord, direction, incoming_box=True)
            if can_push:
                if not incoming_box:
                    del grid[coord]
            return can_push, grid


def score_grid(grid):
    total = 0
    max_x = max([item[0] for item in grid.keys()])
    max_y = max([item[1] for item in grid.keys()])
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in grid and grid[(x, y)] == "O":
                total += (100 * y) + x
    return total


def print_it(grid, robot):
    print(grid)
    max_x = max([item[0] for item in grid.keys()]) + 1
    max_y = max([item[1] for item in grid.keys()]) + 1
    print("max x = ", max_x, "max y = ", max_y)
    for y in range(max_y):
        line = ""
        for x in range(max_x):
            if (x, y) in grid:
                line += grid[(x, y)]
            elif (x, y) == robot:
                line += "@"
            else:
                line += "."
        print(line)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    grid, moves = puzzle_input.split("\n\n")
    grid, robot = get_grid(grid)
    print(grid)
    moves = get_moves(moves)
    for move in moves:
        print(move)
        next_coord = (robot[0] + move[0], robot[1] + move[1])
        if next_coord in grid:
            if grid[next_coord] == "#":
                pass
            elif grid[next_coord] == "O":
                can_move, grid = push_box(grid, next_coord, move)
                if can_move:
                    robot = next_coord
            else:
                raise Exception(f"Invalid object found at {next_coord}")
        else:
            robot = next_coord
    score = score_grid(grid)
    print_it(grid, robot)
    return score


def get_grid_boogaloo(grid_input) -> (dict, tuple[int, int]):
    grid = []
    robot = None
    for y, line in enumerate(grid_input.split("\n")):
        curr_line = []
        for x, char in enumerate(line):
            if char == "#":
                curr_line.extend(["#", "#"])
            elif char == "O":
                curr_line.extend(["[", "]"])
            elif char == "@":
                robot = (2 * x, y)
                curr_line.extend([".", "."])
            else:
                curr_line.extend([".", "."])
        grid.append(curr_line)
    return grid, robot


def score_grid_boogaloo(grid):
    total = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if grid[y][x] == "[":
                total += (100 * y) + x
    return total


def print_it_boogaloo(grid, robot):
    for y, l in enumerate(grid):
        line = ""
        for x, char in enumerate(l):
            if (x, y) == robot:
                line += "@"
            else:
                line += char
        print(line)


def push_box_boogaloo(
    grid: dict,
    coord: tuple,
    direction: tuple,
    current_grid: list,
    is_pushed,
    neighbor_can_move=False,
) -> (bool, dict):

    is_pushed.add(coord)
    this_side = current_grid[coord[1]][coord[0]]
    neighbor_coord = (
        (coord[0] + 1, coord[1]) if this_side == "[" else (coord[0] - 1, coord[1])
    )
    incoming = (
        current_grid[coord[1] - direction[1]][coord[0] - direction[0]]
        if (coord[0] - direction[0], coord[1] - direction[1]) in is_pushed
        else "."
    )

    if current_grid[coord[1]][coord[0]] == ".":  # this side can move
        grid[coord[1]][coord[0]] = incoming
        return True, grid

    elif current_grid[coord[1]][coord[0]] == "#":  # this side can't move
        return False, current_grid

    elif current_grid[coord[1]][coord[0]] in "[]":  # uh....
        next_coord = (coord[0] + direction[0], coord[1] + direction[1])

        if neighbor_can_move:
            can_push, grid = push_box_boogaloo(
                grid,
                next_coord,
                direction,
                current_grid,
                is_pushed,
                neighbor_can_move=False,
            )
            if not can_push:
                return False, current_grid

        elif direction in [(0, 1), (0, -1)]:
            neighbor_can_be_pushed, grid = push_box_boogaloo(
                grid,
                neighbor_coord,
                direction,
                current_grid,
                is_pushed,
                neighbor_can_move=True,
            )
            if not neighbor_can_be_pushed:
                return False, current_grid

        can_push, grid = push_box_boogaloo(
            grid,
            next_coord,
            direction,
            current_grid,
            is_pushed,
            neighbor_can_move=False,
        )
        if not can_push:
            return False, current_grid

        grid[coord[1]][coord[0]] = incoming
        return True, grid


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    grid, moves = puzzle_input.split("\n\n")
    grid, robot = get_grid_boogaloo(grid)
    print_it_boogaloo(grid, robot)
    moves = get_moves(moves)
    for move in moves:
        # print(move)
        # print_it_boogaloo(grid, robot)
        # sleep(0.001)
        next_coord = (robot[0] + move[0], robot[1] + move[1])
        next_char = grid[next_coord[1]][next_coord[0]]
        if next_char == "#":
            pass
        elif next_char in "[]":
            is_pushed = set()
            current_grid = deepcopy(grid)
            can_move, grid = push_box_boogaloo(
                deepcopy(grid), next_coord, move, current_grid, is_pushed
            )
            if can_move:
                robot = next_coord
        elif next_char == ".":
            robot = next_coord
    score = score_grid_boogaloo(grid)
    print_it_boogaloo(grid, robot)
    return score


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
    print(f"Test result = {part_two('inputtest2.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
