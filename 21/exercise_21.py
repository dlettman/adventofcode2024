import time
from collections import deque

import pyperclip

from helpers import helpers
from dataclasses import dataclass
from collections import defaultdict
from functools import cache
from math import inf

NUMERIC_PAD = ["789", "456", "123", "X0A"]

DIRECTION_PAD = ["X^A", "<v>"]

DIRECTIONS_TO_COORDS = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1), 0: "A"}

COORDS_TO_DIRECTIONS = {(1, 0): ">", (-1, 0): "<", (0, -1): "^", (0, 1): "v", 0: "A"}


@dataclass
class Move(object):
    x: int
    y: int
    path: str


def find_char(find_char, grid):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == find_char:
                return (x, y)


NEIGHBORS_ORTH_DIR = [(0, 1), (-1, 0), (0, -1), (1, 0)]

NEIGHBORS_ORTH_NUM = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_zigzag(path):
    seen = set()
    prev = None
    for char in path:
        if char in seen and not prev == char:
            return True
        seen.add(char)
        prev = char
    return False


def build_paths(grid) -> dict:
    paths = defaultdict(dict)
    for start in "".join(grid):
        for end in "".join(grid):

            if start == "X" or end == "X":
                continue

            max_len = None
            start_coord = find_char(start, grid)
            found_all = False
            if start == end:
                paths[start][end] = [""]
                continue

            move_queue = deque([Move(start_coord[0], start_coord[1], "")])
            while move_queue:
                move = move_queue.popleft()
                if "0" in grid:
                    NEIGHBORS_ORTH = NEIGHBORS_ORTH_NUM
                else:
                    NEIGHBORS_ORTH = NEIGHBORS_ORTH_DIR
                for n in NEIGHBORS_ORTH:
                    test_coord = (move.x + n[0], move.y + n[1])
                    if (not helpers.out_of_bounds(test_coord, grid)) and (
                        not grid[test_coord[1]][test_coord[0]] == "X"
                    ):
                        if grid[test_coord[1]][test_coord[0]] == end:
                            path = move.path + COORDS_TO_DIRECTIONS[n]
                            if not max_len:
                                max_len = len(path)
                            if len(path) == max_len:
                                if end in paths[start]:
                                    paths[start][end] += [path]
                                else:
                                    paths[start][end] = [path]
                            elif len(path) > max_len:
                                found_all = True
                                break
                        if found_all:
                            break
                        move_queue.append(
                            Move(
                                test_coord[0],
                                test_coord[1],
                                move.path + COORDS_TO_DIRECTIONS[n],
                            )
                        )
            # lexigraphical sorting is reverse from what actually ends up being the optimal order
            paths[start][end] = [
                item for item in paths[start][end] if not is_zigzag(item)
            ][::-1]
    return paths


# pre bake our paths
num_paths = build_paths(NUMERIC_PAD)
dir_paths = build_paths(DIRECTION_PAD)


def get_keypresses(keys, paths, result, idx=0, prev_key="A", curr_path=""):
    try:
        this_key = keys[idx]
        for path in paths[prev_key][this_key]:
            get_keypresses(
                keys, paths, result, idx + 1, this_key, curr_path + path + "A"
            )
    except IndexError:
        result.append(curr_path)
        return result


@cache
def get_shortest_sequence(keys, depth):
    total = 0
    if depth == 0:
        return len(keys)
    split_keys = keys.split("A")
    for sub_keys in split_keys[0:-1]:
        sub_key = sub_keys + "A"
        key_presses = []
        get_keypresses(sub_key, dir_paths, key_presses)
        shortest = min(
            [get_shortest_sequence(sub_seq, depth - 1) for sub_seq in key_presses]
        )
        total += shortest
    return total


def get_complexity_too(num_presses, code):
    multiplier = int(code[0:3].lstrip("0"))
    return num_presses * multiplier


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    total = 0
    for code in puzzle_input:
        result = []
        get_keypresses(code, num_paths, result)
        for sub_seq in result:
            shortest_dist = get_shortest_sequence(sub_seq, 2)
        total += get_complexity_too(shortest_dist, code)
    return total


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    total = 0
    for code in puzzle_input:
        result = []
        get_keypresses(code, num_paths, result)
        for sub_seq in result:
            shortest_dist = get_shortest_sequence(sub_seq, 25)
        total += get_complexity_too(shortest_dist, code)
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
