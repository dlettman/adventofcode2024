import time

import pyperclip

from helpers import helpers

from collections import Counter


def stone_them_to_death(puzzle_input, blinks):
    stones = Counter(puzzle_input[0].split())
    for n in range(blinks):
        new_stones = Counter()
        for stone, count in stones.items():
            if stone == "0":
                new_stones["1"] += count
            elif len(str(stone)) % 2 == 0:
                stone_a = stone[0:len(stone)//2]
                stone_b = stone[len(stone)//2:]
                for sub_stone in [stone_a, stone_b]:
                    new_stones[str(int(sub_stone))] += count
            else:
                new_stones[str(int(stone) * 2024)] += count
        stones = new_stones
    return sum([int(item) for item in stones.values()])


def part_one(input_filename, blinks=75):
    puzzle_input = helpers.parse_input(input_filename)
    return stone_them_to_death(puzzle_input, blinks=25)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    return stone_them_to_death(puzzle_input, blinks=75)



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
