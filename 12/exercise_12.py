import time
from collections import deque

from helpers import helpers


def get_region(coord, grid):
    search_queue = deque([coord])
    char = grid[coord[1]][coord[0]]
    region = set()
    region.add(coord)
    while search_queue:
        current_step = search_queue.popleft()
        for n in helpers.NEIGHBORS_ORTH:
            test_coord = (current_step[0] + n[0], current_step[1] + n[1])
            if not helpers.out_of_bounds(test_coord, grid):
                if all(
                    [
                        not helpers.out_of_bounds(test_coord, grid),
                        grid[test_coord[1]][test_coord[0]] == char,
                        test_coord not in region,
                    ]
                ):
                    region.add(test_coord)
                    search_queue.append(test_coord)
    return region


def get_perimeter(region):
    perimeter = 0
    for coord in region:
        for n in helpers.NEIGHBORS_ORTH:
            if (coord[0] + n[0], coord[1] + n[1]) not in region:
                perimeter += 1
    return perimeter


# We know a space is an outer corner if both neighbor values are NOT in the region
OUTER_CORNERS = [
    {(-1, 0), (0, -1)},  # bottom left
    {(1, 0), (0, -1)},  # bottom right
    {(-1, 0), (0, 1)},  # top left
    {(1, 0), (0, 1)},  # top right
]


# We know a space is an inner corner if the key is NOT in the region, but both of the values are
INNER_CORNERS = {
    (1, 1): {(1, 0), (0, 1)},
    (-1, -1): {(-1, 0), (0, -1)},
    (1, -1): {(1, 0), (0, -1)},
    (-1, 1): {(-1, 0), (0, 1)},
}


def get_sides(region):
    total = 0
    for x, y in region:
        outside_region = set(
            [n for n in helpers.NEIGHBORS if (x + n[0], y + n[1]) not in region]
        )
        total += sum(
            [
                1
                for inner_corner, cant_be_theres in INNER_CORNERS.items()
                if inner_corner in outside_region
                and not cant_be_theres.intersection(outside_region)
            ]
        )
        total += sum([1 for corner in OUTER_CORNERS if corner.issubset(outside_region)])
    return total


def score_regions(regions, perimeter=True):
    if perimeter:
        return sum([get_perimeter(region) * len(region) for region in regions])
    else:
        return sum([get_sides(region) * len(region) for region in regions])


def do_it(puzzle_input, perimeter=True):
    seen = set()
    regions = []
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if (x, y) not in seen:
                region = get_region((x, y), puzzle_input)
                seen = seen.union(region)
                regions.append(region)
    return score_regions(regions, perimeter=perimeter)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    return do_it(puzzle_input, perimeter=True)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    return do_it(puzzle_input, perimeter=False)


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
