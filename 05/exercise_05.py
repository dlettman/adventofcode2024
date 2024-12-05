import time

import pyperclip

from helpers import helpers


def get_rules_and_updates(puzzle_input):
    updating = False
    not_before = {}
    updates = []
    for line in puzzle_input:
        if not line:
            updating = True
            continue
        elif not updating:
            a, b = line.split("|")
            if a not in not_before:
                not_before[a] = {b}
            else:
                not_before[a].add(b)
        elif updating:
            updates.append(line.split(','))
    return not_before, updates


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    not_before, updates = get_rules_and_updates(puzzle_input)
    total = 0
    for line in updates:
        ok = True
        seen = set()
        for num in line:
            if num in not_before:
                if not_before[num].intersection(seen):
                    ok = False
                    break
            seen.add(num)
        if ok:
            total += int(line[len(line)//2])
    return total


def stupid_sort(nums, not_before):
    seen = set()
    for idx, item in enumerate(nums):
        if item in not_before:
            if not_before[item].intersection(seen):
                nums.pop(idx)
                nums.insert(idx - 1, item)
                return stupid_sort(nums, not_before)
        seen.add(item)
    return nums


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    not_before, updates = get_rules_and_updates(puzzle_input)
    total = 0
    for line in updates:
        needs_some_sorting = False
        seen = set()
        for num in line:
            if num in not_before:
                if not_before[num].intersection(seen):
                    needs_some_sorting = True
                    break
            seen.add(num)
        if needs_some_sorting:
            line = stupid_sort(line, not_before)
            total += int(line[len(line)//2])
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
