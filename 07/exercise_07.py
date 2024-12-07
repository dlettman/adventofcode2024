import time

import pyperclip

from helpers import helpers


def get_targets_and_terms(puzzle_input):
    targets, terms = [], []
    for line in puzzle_input:
        target, terms_chunk = line.split(":")
        terms_chunks = terms_chunk.split()
        targets.append(target)
        terms.append(terms_chunks)
        return targets, terms

one_operators = ["+", "*"]

def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    targets, terms = get_targets_and_terms(puzzle_input)
    total = 0
    for target, term in zip(targets, terms):
        combinations = [term]
        new_combinations = []
        for sub_term in terms:
            for combination in combinations:
                new_combinations.append(combination + "+" + sub_term)
                new_combinations.append(combination + "*" + sub_term)
            combinations = new_combinations
        for combination in combinations:
            if eval(combination) == target:
                total += target
    return total


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    targets, terms = get_targets_and_terms(puzzle_input)
    total = 0
    for target, term in zip(targets, terms):
        combinations = [term]
        new_combinations = []
        for sub_term in terms:
            for combination in combinations:
                new_combinations.append(combination + "+" + sub_term)
                new_combinations.append(combination + "*" + sub_term)
                new_combinations.append(combination + sub_term)
            combinations = new_combinations
        for combination in combinations:
            if eval(combination) == target:
                total += target
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
