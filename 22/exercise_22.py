import time
from collections import Counter, deque

from helpers import helpers


def mix(sn, num) -> int:
    return sn ^ num


def prune(sn) -> int:
    return sn % 16777216


def get_next_sn(sn) -> int:
    mixer = sn * 64
    sn = mix(mixer, sn)
    sn = prune(sn)

    mixer = sn // 32
    sn = mix(mixer, sn)
    sn = prune(sn)

    mixer = sn * 2048
    sn = mix(mixer, sn)
    sn = prune(sn)
    return sn


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    puzzle_input = [int(item) for item in puzzle_input]
    total = 0
    for num in puzzle_input:
        sn = num
        for n in range(2000):
            sn = get_next_sn(sn)
        total += sn
    return total


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    puzzle_input = [int(item) for item in puzzle_input]
    payoffs = Counter()
    for num in puzzle_input:
        monkey_best_price = dict()
        sn = num
        deltas = deque()
        prices = deque([sn % 10])
        for n in range(2000):
            sn = get_next_sn(sn)
            prices.append(sn % 10)
            if len(prices) > 1:
                deltas.append(prices[-1] - prices[-2])
            if len(deltas) > 4:
                deltas.popleft()
            if len(deltas) == 4:
                if tuple(deltas) not in monkey_best_price:
                    monkey_best_price[tuple(deltas)] = prices[-1]
        for deltas in monkey_best_price:
            payoffs[deltas] += monkey_best_price[deltas]
    return payoffs.most_common(1)


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
