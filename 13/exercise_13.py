import re
import time
from dataclasses import dataclass
from math import inf

import z3

from helpers import helpers


@dataclass
class ClawConfig:
    a: tuple[int, int] = None
    b: tuple[int, int] = None
    prize: tuple[int, int] = None


BUTTON_REGEX = ".*X\\+(\\d+).*Y\\+(\\d+)"
PRIZE_REGEX = ".*X=(\\d+).*Y=(\\d+)"


def get_configs(puzzle_input, num_big=False):
    chunks = puzzle_input.split("\n\n")
    configs = []
    for lines in chunks:
        current_config = ClawConfig()
        lines = lines.split("\n")
        x, y = re.search(BUTTON_REGEX, lines[0]).groups()
        current_config.a = (int(x), int(y))
        x, y = re.search(BUTTON_REGEX, lines[1]).groups()
        current_config.b = (int(x), int(y))
        x, y = re.search(PRIZE_REGEX, lines[2]).groups()
        current_config.prize = (int(x), int(y)) if not num_big else (int(x) + 10000000000000, int(y) + 10000000000000)
        configs.append(current_config)
    return configs


def find_min_unga(config, reps=1000000000000):
    best_value = inf
    for n in range(reps):
        location = [n * config.a[0], n * config.a[1]]
        if tuple(location) == config.prize:
            best_value = min([best_value, n * 3])
        elif any([location[0] > config.prize[0], location[1] > config.prize[1]]):
            break
        for m in range(reps):
            location = [n * config.a[0], n * config.a[1]]
            location[0] += m * config.b[0]
            location[1] += m * config.b[1]
            if tuple(location) == config.prize:
                best_value = min([best_value, (n * 3 + m)])
            elif any([location[0] > config.prize[0], location[1] > config.prize[1]]):
                break
    return best_value if not best_value == inf else 0


def find_min_smartyman(config):
    a_x, a_y = config.a
    b_x, b_y = config.b
    p_x, p_y = config.prize

    solver = z3.Optimize()
    a, b = z3.Int('a'), z3.Int('b')
    solver.add(a_x * a + b_x * b == p_x)
    solver.add(a_y * a + b_y * b == p_y)
    solver.minimize(a * 3 + b)

    if solver.check() == z3.sat:
        m = solver.model()
        return m.eval(a).as_long() * 3 + m.eval(b).as_long()
    else:
        return 0


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    configs = get_configs(puzzle_input)
    return sum([find_min_unga(config, reps=100000) for config in configs])


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    configs = get_configs(puzzle_input, num_big=True)
    return sum([find_min_smartyman(config) for config in configs])


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
