import re
import time
from dataclasses import dataclass
from math import prod

from helpers import helpers


@dataclass
class Robot(object):
    p = tuple[int, int]
    v = tuple[int, int]

    def __init__(self, p, v):
        self.p = p
        self.v = v


ROBO_REGEX = "p=([\\-0-9]+),([\\-0-9]+).*v=([\\-0-9]+),([\\-0-9]+)"


def robot_roll_call(puzzle_input):
    robots = []
    for line in puzzle_input:
        p_x, p_y, v_x, v_y = re.search(ROBO_REGEX, line).groups()
        robots.append(Robot(p=(int(p_x), int(p_y)), v=(int(v_x), int(v_y))))
    return robots


def part_one(input_filename, seconds=100, width=11, height=7):
    puzzle_input = helpers.parse_input(input_filename)
    robots = robot_roll_call(puzzle_input)
    for robot in robots:
        final_pos = (
            (robot.p[0] + robot.v[0] * seconds) % width,
            (robot.p[1] + robot.v[1] * seconds) % height,
        )
        robot.p = final_pos
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        if robot.p[0] < (width // 2):
            if robot.p[1] < (height // 2):
                quadrants[0] += 1
            elif robot.p[1] > (height // 2):
                quadrants[1] += 1
        elif robot.p[0] > (width / 2):
            if robot.p[1] < (height // 2):
                quadrants[2] += 1
            elif robot.p[1] > (height // 2):
                quadrants[3] += 1
    return prod(quadrants)


def print_it(robots, width=11, height=7):
    for y in range(height + 1):
        line = ""
        for x in range(width + 1):
            if (x, y) in robots:
                line += "#"
            else:
                line += "."
        print(line)


def part_two(input_filename, seconds=100000000, width=11, height=7):
    puzzle_input = helpers.parse_input(input_filename)
    robots = robot_roll_call(puzzle_input)
    for n in range(seconds):
        for robot in robots:
            final_pos = (
                (robot.p[0] + robot.v[0]) % width,
                (robot.p[1] + robot.v[1]) % height,
            )
            robot.p = final_pos

        # Lots of trial and error goes here

        positions = set(robot.p for robot in robots)
        if len(positions) == len(puzzle_input):
            print("!!!")
            print(n + 1)
            print("!!!")
            print_it(positions, width, height)
            print("!!!")
            return n + 1


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    onestart = time.time()
    p1result = part_one("input.txt", width=101, height=103)
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    print(f"Time = {oneend - onestart}")
    print("\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt", width=101, height=103)
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
