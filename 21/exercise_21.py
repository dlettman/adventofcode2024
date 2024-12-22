import time

import pyperclip

from helpers import helpers
from collections import deque
from dataclasses import dataclass
from functools import cache

NUMERIC_PAD = ("789", "456", "123", "X0A")

DIRECTION_PAD = ("X^A", "<v>")

DIRECTIONS_TO_COORDS = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

COORDS_TO_DIRECTIONS = {(1, 0): ">", (-1, 0): "<", (0, -1): "^", (0, 1): "v"}

# NEIGHBORS_ORTH_NUM = [(1, 0),  (0, 1), (-1, 0), (0, -1)]
TRAD_NEIGHBORS_ORTH_NUM = ((0, -1), (-1, 0), (1, 0), (0, 1))
INVERTED_NEIGHBORS_ORTH_NUM = ((0, 1), (-1, 0), (1, 0), (0, -1))

# NEIGHBORS_ORTH_NUM = []

NEIGHBORS_ORTH_DIRECTION = ((1, 0), (0, 1), (0, -1), (-1, 0))
# NEIGHBORS_ORTH_DIRECTION = [(1, 0), (0, 1), (-1, 0), (0, -1)]


@dataclass
class Move(object):
    x: int
    y: int
    path: list[tuple[int, int]]


class Robot(object):

    def __init__(self, robo_type: str):
        self.robo_type = robo_type
        if self.robo_type == "numeric":
            self.grid = NUMERIC_PAD
        elif self.robo_type == "direction":
            self.grid = DIRECTION_PAD
        else:
            raise Exception("Invalid Robot Type")
        self.pos = get_coord_of_symbol("A", self.grid)
        self.next_bot = None

    def __repr__(self):
        return f"Bot: {self.robo_type}, {self.symbol}, Next: {self.next_bot.robo_type if self.next_bot else 'None'}"

    @property
    def symbol(self):
        if self.robo_type == "numeric":
            return NUMERIC_PAD[self.pos[1]][self.pos[0]]
        elif self.robo_type == "direction":
            return DIRECTION_PAD[self.pos[1]][self.pos[0]]

    def generate_moves_and_reposition(self, goal_symbol, non, output_moves=None):
        if self.robo_type == "numeric":
            moves = get_next_button_presses_numeric(self.symbol, goal_symbol, non=non)
        else:
            moves = get_next_button_presses_direction(self.symbol, goal_symbol, num=False, non=non)
        if self.next_bot:
            for move in moves:
                if self.next_bot:
                    self.next_bot.generate_moves_and_reposition(move, non, output_moves=output_moves)
                    if self.robo_type == "numeric":
                        self.pos = get_coord_of_symbol(goal_symbol, NUMERIC_PAD)
                    else:
                        self.pos = get_coord_of_symbol(goal_symbol, DIRECTION_PAD)
        else:
            output_moves += moves
            self.pos = get_coord_of_symbol(goal_symbol, DIRECTION_PAD)
        return


@cache
def generate_moves_and_reposition_too(bot, goal_symbol, non, output_moves=None):
    if bot.robo_type == "numeric":
        moves = get_next_button_presses_numeric(bot.symbol, goal_symbol, non=non)
    else:
        moves = get_next_button_presses_direction(bot.symbol, goal_symbol, num=False, non=non)
    if bot.next_bot:
        for move in moves:
            if bot.next_bot:
                output_moves = generate_moves_and_reposition_too(bot.next_bot, move, non, output_moves=output_moves)
                if bot.robo_type == "numeric":
                    bot.pos = get_coord_of_symbol(goal_symbol, NUMERIC_PAD)
                else:
                    bot.pos = get_coord_of_symbol(goal_symbol, DIRECTION_PAD)
    else:
        output_moves += len(moves)
        bot.pos = get_coord_of_symbol(goal_symbol, DIRECTION_PAD)
    return output_moves


@cache
def get_coord_of_symbol(symbol, grid):
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == symbol:
                return (x, y)
    raise Exception(f"Symbol {symbol} not found in grid {grid}")


@cache
def find_path_to_symbol(
    start, symbol, grid, num=True, non=None
) -> list[tuple[int, int]]:  # returns a list of the deltas
    move_queue = deque([Move(*start, [])])
    while move_queue:
        move = move_queue.popleft()
        if num:
            NEIGHBORS_ORTH = non
        else:
            NEIGHBORS_ORTH = NEIGHBORS_ORTH_DIRECTION
        for n in NEIGHBORS_ORTH:
            test_coord = (move.x + n[0], move.y + n[1])
            if (not helpers.out_of_bounds(test_coord, grid)) and (
                not grid[test_coord[1]][test_coord[0]] == "X"
            ):
                if grid[test_coord[1]][test_coord[0]] == symbol:
                    return move.path + [n]
                move_queue.append(Move(test_coord[0], test_coord[1], move.path + [n]))

@cache
def get_next_button_presses_numeric(current, goal_symbol, non=None) -> list[str]:
    if current == goal_symbol:
        return ["A"]
    start = get_coord_of_symbol(current, NUMERIC_PAD)
    path = find_path_to_symbol(start, goal_symbol, NUMERIC_PAD, num=True, non=non)
    return [COORDS_TO_DIRECTIONS[coord] for coord in path] + ["A"]

    # for coord in path:
    #     yield COORDS_TO_DIRECTIONS[coord]
    # raise StopIteration

@cache
def get_next_button_presses_direction(
    current, goal_symbol, num=False, non=None
) -> list[str]:
    if current == goal_symbol:
        return ["A"]
    start = get_coord_of_symbol(current, DIRECTION_PAD)
    path = find_path_to_symbol(start, goal_symbol, DIRECTION_PAD, num=False)
    return [COORDS_TO_DIRECTIONS[coord] for coord in path] + ["A"]

    # for coord in path:
    #     yield COORDS_TO_DIRECTIONS[coord]
    # raise StopIteration


def get_complexity(buttons, code):
    multiplier = int(code[0:3].lstrip("0"))
    return len(buttons) * multiplier

def get_complexity_too(buttons, code):
    multiplier = int(code[0:3].lstrip("0"))
    return buttons * multiplier


def part_one(input_filename):
    # puzzle_input = helpers.parse_input(input_filename)
    # r1 = Robot("numeric")
    # r2, r3 = Robot("direction"), Robot("direction")
    # total = 0
    # for code in puzzle_input:
    #     complexity = None
    #     for non in [INVERTED_NEIGHBORS_ORTH_NUM, TRAD_NEIGHBORS_ORTH_NUM]:
    #         human_presses = []
    #         for char in code:
    #             r2_presses = get_next_button_presses_numeric(r1.symbol, char, non=non)
    #             for r2_press in r2_presses:
    #                 r3_presses = get_next_button_presses_direction(
    #                     r2.symbol, r2_press, non=non
    #                 )
    #                 for r3_press in r3_presses:
    #                     human_presses += get_next_button_presses_direction(
    #                         r3.symbol, r3_press, non=non
    #                     )
    #                     r3.pos = get_coord_of_symbol(r3_press, DIRECTION_PAD)
    #
    #                 r2.pos = get_coord_of_symbol(r2_press, DIRECTION_PAD)
    #
    #             r1.pos = get_coord_of_symbol(char, NUMERIC_PAD)
    #
    #         if not complexity:
    #             complexity = get_complexity(human_presses, code)
    #         else:
    #             complexity = min(complexity, get_complexity(human_presses, code))
    #     total += complexity
    # return total

    puzzle_input = helpers.parse_input(input_filename)
    direction_bots = [Robot("numeric")]
    direction_bots += [Robot("direction") for _ in range(2)]
    for idx, bot in enumerate(direction_bots):
        try:
            bot.next_bot = direction_bots[idx + 1]
        except IndexError:
            bot.next_bot = None
    # print(direction_bots)
    total = 0
    for code in puzzle_input:
        complexity = None
        for non in [INVERTED_NEIGHBORS_ORTH_NUM, TRAD_NEIGHBORS_ORTH_NUM]:
            human_presses = []
            for char in code:
                output_moves = []
                direction_bots[0].generate_moves_and_reposition(char, non=non, output_moves=output_moves)
                human_presses += output_moves
            if not complexity:
                complexity = get_complexity(human_presses, code)
            else:
                new_complexity = get_complexity(human_presses, code)
                print("oc = ", complexity, ", nc = ", new_complexity)
                complexity = min(complexity, get_complexity(human_presses, code))
            print(len(human_presses))

        print(complexity)
        print(len(human_presses))
        print(human_presses)
        total += complexity
    return total

def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    direction_bots = [Robot("numeric")]
    direction_bots += [Robot("direction") for _ in range(25)]
    for idx, bot in enumerate(direction_bots):
        try:
            bot.next_bot = direction_bots[idx + 1]
        except IndexError:
            bot.next_bot = None
    total = 0
    for code in puzzle_input:
        complexity = None
        for non in [INVERTED_NEIGHBORS_ORTH_NUM, TRAD_NEIGHBORS_ORTH_NUM]:
            human_presses = 0
            for char in code:
                output_moves = 0
                output_moves = generate_moves_and_reposition_too(direction_bots[0], char, non=non, output_moves=output_moves)
                print("received ", output_moves)
                human_presses += output_moves
            if not complexity:
                complexity = get_complexity_too(human_presses, code)
            else:
                new_complexity = get_complexity_too(human_presses, code)
                print("oc = ", complexity, ", nc = ", new_complexity)
                complexity = min(complexity, get_complexity_too(human_presses, code))

        print(complexity)
        print(human_presses)
        total += complexity
    return total


    # TODO: Update robots to take in a list, generate a new list based off of that, then update their own position. Do that down the row and baby, you got a stew going


if __name__ == "__main__":
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # onestart = time.time()
    # p1result = part_one("input.txt")
    # oneend = time.time()
    # print(f"REAL RESULT = {p1result}")
    # print(f"Time = {oneend - onestart}")
    # print("\n")
    print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
