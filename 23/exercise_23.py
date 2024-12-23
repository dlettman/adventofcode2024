import time

import pyperclip

from helpers import helpers


def one_starts_with_t(tup):
    for item in tup:
        if item.startswith("t"):
            return True
    return False


def make_connections(puzzle_input):
    connections = {}
    for line in puzzle_input:
        a, b = sorted(line.split("-"))
        if not a in connections:
            connections[a] = {b}
        else:
            connections[a].add(b)
    return connections

def make_triplets(connections):
    triplets = set()
    for origin, dests in connections.items():
        for dest in dests:
            if dest in connections:
                for dest_dest in connections[dest]:
                    if (dest_dest in connections and origin in connections[dest_dest]) or (dest_dest in connections[origin]):
                        triplets.add(tuple(sorted([origin, dest, dest_dest])))
    return triplets

def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    connections = make_connections(puzzle_input)
    triplets = make_triplets(connections)
    return (sum([1 for item in triplets if one_starts_with_t(item)]))


def is_connected(a, b, connections):
    return (a in connections and b in connections[a]) or (b in connections and a in connections[b])


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    connections = make_connections(puzzle_input)
    super_groups = make_triplets(connections)
    added_a_new_one = True
    max_len = 3
    while True:
        print(sorted(list(super_groups), key=lambda x: len(x))[-1])
        new_super_groups = super_groups.copy()
        for super_group in super_groups:
            working_supergroup = sorted(list(super_group))
            for member in working_supergroup:
                if member in connections:
                    for potential_member in connections[member]:
                        if potential_member in working_supergroup:
                            continue
                        new_connection = False
                        for other_sg_member in working_supergroup:
                            if other_sg_member == member:
                                continue
                            if not is_connected(potential_member, other_sg_member, connections):
                                new_connection = False
                                break
                            elif is_connected(potential_member, other_sg_member, connections):
                                new_connection = True
                        if new_connection:
                            new_super_group = tuple(list(super_group) + [potential_member])
                            new_super_groups.add(tuple(sorted(new_super_group)))
                            added_a_new_one = True
                            break
                    if added_a_new_one:
                        break
        if added_a_new_one:
            super_groups = new_super_groups
        new_max_len = max(len(item) for item in super_groups)
        if new_max_len == max_len:
            return ",".join(sorted(list(super_groups), key=lambda x: len(x))[-1])
        max_len = new_max_len


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
