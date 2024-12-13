import time

import pyperclip

from helpers import helpers


def get_rules_and_updates(puzzle_input):
    updating = False
    must_be_before = {}
    updates = []
    for line in puzzle_input:
        if not line:
            updating = True
            continue
        elif not updating:
            a, b = line.split("|")
            if a not in must_be_before:
                must_be_before[a] = {b}
            else:
                must_be_before[a].add(b)
        elif updating:
            updates.append(line.split(","))
    return must_be_before, updates


def needs_sorting(line, must_be_before):
    seen = set()
    for num in line:
        if num in must_be_before:
            if must_be_before[num].intersection(seen):
                return True
        seen.add(num)
    return False


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    must_be_before, updates = get_rules_and_updates(puzzle_input)
    return sum(
        [
            int(line[len(line) // 2])
            for line in updates
            if not needs_sorting(line, must_be_before)
        ]
    )


def stupid_sort(nums, must_be_before):
    seen = set()
    for idx, item in enumerate(nums):
        if item in must_be_before:
            if must_be_before[item].intersection(seen):
                nums.pop(idx)
                nums.insert(idx - 1, item)
                return stupid_sort(nums, must_be_before)
        seen.add(item)
    return nums


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    must_be_before, updates = get_rules_and_updates(puzzle_input)
    return sum(
        [
            int(stupid_sort(line, must_be_before)[len(line) // 2])
            for line in updates
            if needs_sorting(line, must_be_before)
        ]
    )


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
