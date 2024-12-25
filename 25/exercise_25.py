import time

from helpers import helpers


def get_keys_and_locks(puzzle_input):
    puzzle_input = puzzle_input.split("\n\n")
    keys = []
    locks = dict()
    for schematic in puzzle_input:
        schematic = schematic.splitlines()
        columns = [[row[n] for row in schematic] for n in range(5)]
        current_dict = keys if columns[0][0] == "#" else locks
        if current_dict == locks:
            for column in columns:
                length = column.count("#")
                current_dict = current_dict.setdefault(length, {})
        else:
            key = [column.count("#") for column in columns]
            keys.append(key)
    return keys, locks


def find_matches_recursively(current_dict, key, depth=0):
    if depth == 5:
        return 1
    total = 0
    for n in range(8 - key[depth]):
        try:
            total += find_matches_recursively(current_dict[n], key, depth + 1)
        except KeyError:
            continue
    return total


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    keys, locks = get_keys_and_locks(puzzle_input)
    return sum([find_matches_recursively(locks, key) for key in keys])


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    onestart = time.time()
    p1result = part_one("input.txt")
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    print(f"Time = {oneend - onestart}")
