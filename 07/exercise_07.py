import time

import pyperclip

import helpers


def get_targets_and_terms(puzzle_input):
    targets, terms = [], []
    for line in puzzle_input:
        target, terms_chunk = line.split(":")
        terms_chunks = terms_chunk.split()
        targets.append(int(target))
        terms.append([int(item) for item in terms_chunks])
    return targets, terms


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    targets, list_of_terms = get_targets_and_terms(puzzle_input)
    total = 0
    # print(targets, terms)

    for target, terms in zip(targets, list_of_terms):
        combinations = [terms[0]]
        for term in terms[1:]:
            new_combinations = []
            for combination in combinations:
                new_comb = combination + term
                if new_comb <= target:
                    new_combinations.append(new_comb)
                new_comb = combination * term
                if new_comb <= target:
                    new_combinations.append(new_comb)
            combinations = new_combinations.copy()
        for combination in combinations:
            if combination == target:
                total += target
                break
    return total


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    targets, list_of_terms = get_targets_and_terms(puzzle_input)
    total = 0
    print(targets, terms)

    for target, terms in zip(targets, list_of_terms):
        combinations = [terms[0]]
        for term in terms[1:]:
            new_combinations = []
            for combination in combinations:
                new_comb = combination + term
                if new_comb <= target:
                    new_combinations.append(new_comb)
                new_comb = combination * term
                if new_comb <= target:
                    new_combinations.append(new_comb)
                new_comb = int(str(combination) + str(term))
                if new_comb <= target:
                    new_combinations.append(new_comb)
            combinations = new_combinations.copy()
        for combination in combinations:
            if combination == target:
                total += target
                break
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
