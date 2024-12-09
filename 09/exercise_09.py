import time

import pyperclip

from helpers import helpers


def write_files(puzzle_input):
    disk = []
    file = True
    for idx, char in enumerate(puzzle_input[0]):
        # print(idx, char)
        for _ in range(int(char)):
            if file:
                disk.append(idx // 2)
            else:
                disk.append(".")
        file = not file
    return disk

def total_up(disk):
    total = 0
    for idx, value in enumerate(disk):
        if value == ".":
            continue
        else:
            total += idx * value
    return total

def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    disk = write_files(puzzle_input)
    l_pointer, r_pointer = 0, len(disk) - 1
    while l_pointer < r_pointer:
        while disk[l_pointer] != "." and l_pointer < r_pointer:
            l_pointer += 1
        while disk[r_pointer] == "." and r_pointer > l_pointer:
            r_pointer -= 1
        disk[l_pointer] = disk[r_pointer]
        disk[r_pointer] = "."
    return total_up(disk)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    disk = write_files(puzzle_input)
    current_file = len(puzzle_input[0]) // 2
    while current_file > 0:
        r_pointer = len(disk) - 1
        while not disk[r_pointer] == current_file and r_pointer >= 0:
            r_pointer -= 1
        file_end_idx = r_pointer
        """
        Scan from the end of the disk backwards looking for the file of interest
        """
        while disk[r_pointer - 1] == current_file:
            r_pointer -= 1
        file_start_idx = r_pointer
        file_length = (file_end_idx - file_start_idx) + 1
        l_pointer = 0
        empty_space = 0
        empty_space_start = None
        while l_pointer < file_start_idx:
            """
            Search for a big enough chunk of empty space
            """
            if not disk[l_pointer] == ".":
                empty_space = 0
                empty_space_start = None
                l_pointer += 1
            else:  # empty space
                empty_space += 1
                empty_space_start = empty_space_start if empty_space_start else l_pointer
                l_pointer += 1
            if empty_space == file_length:
                """
                Write file
                """
                for n in range(file_length):
                    disk[empty_space_start + n] = current_file
                """
                Delete file
                """
                for n in range(file_length):
                    disk[file_start_idx + n] = "."
                break
        current_file -= 1
    return total_up(disk)



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
