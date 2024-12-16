import time

import pyperclip

from helpers import helpers
from itertools import cycle
import heapq
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Move:
    score: int
    x: int
    y: int
    dir: tuple[int, int]
    path: list[tuple[int, int]]

    def __lt__(self, other):
        return self.score < other.score

def get_grid(puzzle_input):
    grid = defaultdict(lambda: 0)
    start = None
    exit = None
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if char == "#":
                grid[(x, y)] = "#"
            elif char == "E":
                exit = (x, y)
            elif char == "S":
                start = (x, y)
    return grid, start, exit


DIRS = [(1, 0), (0, -1), (-1, 0), (0, 1)]
def get_dir(idx):
    return DIRS[idx % len(DIRS)]

def get_num_of_turns(start_dir, end_dir):
    if start_dir == end_dir:
        return 0
    start_idx = None
    for idx, dir in enumerate(DIRS):
        if dir == start_dir:
            start_idx = idx
            break
    for n in [1, -1]:
        if DIRS[(start_idx + n) % len(DIRS)] == end_dir:
            return 1
    return 2

def its_dijkstra_time(grid, start, exit):
    queue = [Move(0, start[0], start[1], (1, 0), [start])] # score, x, y, dir_idx
    # print(grid)
    while True:
        move = heapq.heappop(queue)
        # print(move)
        for delta_x, delta_y in helpers.NEIGHBORS_ORTH:
            new_x, new_y = move.x + delta_x, move.y + delta_y
            if grid[(new_x, new_y)] == "#":
                continue
            if not grid[new_x, new_y, (delta_x, delta_y)]:
                new_dir = delta_x, delta_y
                turns = get_num_of_turns(move.dir, new_dir)
                new_space_score = move.score + 1 + 1000 * turns
                grid[(new_x, new_y, (delta_x, delta_y))] = new_space_score
                if (new_x, new_y) == exit:
                    return new_space_score
                heapq.heappush(queue, Move(new_space_score, new_x, new_y, new_dir, move.path + [(new_x, new_y)]))


def its_dijkstra_time_too(grid, start, exit):
    queue = [Move(0, start[0], start[1], (1, 0), [start])] # score, x, y, dir_idx
    # print(grid)
    optimal_path_spaces = set()
    optimal_score = 0
    while queue:
        move = heapq.heappop(queue)
        if optimal_score != 0 and move.score > optimal_score:
            continue
        for delta_x, delta_y in helpers.NEIGHBORS_ORTH:
            new_x, new_y = move.x + delta_x, move.y + delta_y
            if grid[(new_x, new_y)] == "#":
                continue
            if (not grid[new_x, new_y, (delta_x, delta_y)]) or (grid[new_x, new_y, (delta_x, delta_y)]) or  ((new_x, new_y) == exit):
                new_dir = delta_x, delta_y
                turns = get_num_of_turns(move.dir, new_dir)
                new_space_score = move.score + 1 + 1000 * turns
                grid[(new_x, new_y, (delta_x, delta_y))] = new_space_score
                if (new_x, new_y) == exit:
                    if not optimal_score:
                        optimal_score = new_space_score
                    for space in move.path:
                        optimal_path_spaces.add(space)
                heapq.heappush(queue, Move(new_space_score, new_x, new_y, new_dir, move.path + [(new_x, new_y)]))
    return len(optimal_path_spaces)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grid, start, exit = get_grid(puzzle_input)
    current_dir_idx = 0
    return its_dijkstra_time(grid, start, exit)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grid, start, exit = get_grid(puzzle_input)
    current_dir_idx = 0
    return its_dijkstra_time_too(grid, start, exit)


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
