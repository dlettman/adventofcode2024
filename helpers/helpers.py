import argparse

# import curses
import os
import pathlib
import re
import shutil
import time

import html2text
import pyperclip
import requests

#
# def init_curses():
#     scr = curses.initscr()
#     curses.curs_set(False)
#     curses.start_color()
#     curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
#     curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
#     curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
#     curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
#     scr.scrollok(False)
#     return scr


YEAR = "2024"
BASE_URL = f"https://adventofcode.com/"

NEIGHBORS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
NEIGHBORS_ORTH = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_input(filename):
    with open(filename) as file:
        input_list = file.read().splitlines()
    return input_list


def nested_list_to_int(input_data):
    return [[int(x) for x in lst] for lst in input_data]


def out_of_bounds(coord, map):
    return any(
        [
            coord[0] < 0,
            coord[1] < 0,
            coord[0] > (len(map[0]) - 1),
            coord[1] > (len(map) - 1),
        ]
    )


class Coordinate(object):
    def __init__(self, *coordinate_tuple):
        if len(coordinate_tuple) == 1:
            try:
                self.data = tuple(coordinate_tuple[0])
            except TypeError:
                self.data = tuple(coordinate_tuple)
        else:
            self.data = tuple([item for item in coordinate_tuple])

    @property
    def x(self):
        if not self.data:
            return None
        else:
            return self.data[0]

    @x.setter
    def x(self, value):
        self.__setitem__(0, value)

    @property
    def y(self):
        if len(self.data) < 2:
            return None
        else:
            return self.data[1]

    @y.setter
    def y(self, value):
        self.__setitem__(1, value)

    @property
    def z(self):
        if len(self.data) < 3:
            return None
        else:
            return self.data[1]

    @z.setter
    def z(self, value):
        self.__setitem__(2, value)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        if not len(self) == len(other):
            raise IndexError(
                "Coordinate addition not supported for objects of different length"
            )
        return Coordinate([self.data[n] + other[n] for n in range(len(self))])

    def __sub__(self, other):
        if not len(self) == len(other):
            raise IndexError(
                "Coordinate subtraction not supported for objects of different length"
            )

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        if len(self.data) < (key - 1):
            raise IndexError(f"Coordinate is {len(self.data)}-dimensional")
        data_list = list(self.data)  # make a mutable copy
        data_list[key] = value
        self.data = tuple(data_list)


def display_output(
    part1_func=None,
    part1_test=True,
    part1=True,
    part2_func=None,
    part2_test=True,
    part2=True,
):
    p1result, p2result = None, None
    if any([part1, part1_test]):
        print("*** PART ONE ***\n")
        if part1_test:
            print(f"Test result = {part1_func('inputtest.txt')}\n")
        if part1:
            onestart = time.time()
            p1result = part2_func("input.txt")
            oneend = time.time()
            print(f"REAL RESULT = {p1result}")
            print(f"Time = {oneend - onestart}")
    if any([part2, part2_test]):
        print("\n*** PART TWO ***\n")
        if part2_test:
            print(f"Test result = {part2_func('inputtest.txt')}\n")
        if part2:
            twostart = time.time()
            p2result = part2_func("input.txt")
            twoend = time.time()
            print(f"REAL RESULT = {p2result}")
            print(f"Time = {twoend - twostart}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)


def create_folder_structure():
    cwd = pathlib.Path().resolve()
    for i in range(1, 26):
        day_number = str(i).zfill(2)
        newdir_path = os.path.join(cwd, day_number)

        try:
            os.mkdir(newdir_path)
        except FileExistsError:
            pass

        for filename in ["inputtest.txt", "input.txt"]:
            pathlib.Path(os.path.join(newdir_path, filename)).touch()

        exercise_filename = f"exercise_{day_number}.py"
        shutil.copy(
            (os.path.join(cwd, "template.py")),
            os.path.join(newdir_path, exercise_filename),
        )


def download_problem_for_day(day, year=YEAR):
    year = year if year else YEAR
    day_url = BASE_URL + f"{year}/day/{str(day)}"
    gh_cookie = os.environ.get("GH_COOKIE")
    day_number = str(day).zfill(2)
    cwd = pathlib.Path().resolve()

    response = requests.get(day_url, headers={"cookie": gh_cookie})
    parsed_response = html2text.html2text(response.text)

    # drop header nonsense
    print("*******")
    print(parsed_response)
    parsed_response = parsed_response.split("## \\")[1]

    # extract example
    text = response.text
    example_start = text.split("For example")[1]
    regex = "<pre><code>(.*?)</code></pre>"
    example = re.findall(regex, example_start, re.DOTALL)[-1].strip("\n")
    example = "\n".join([item for item in example.split("\n")])
    example_path = os.path.join(cwd, day_number, f"inputtest.txt")
    with open(example_path, "w+") as file:
        file.write(example)

    # get problem text
    parsed_response = parsed_response.split("To play, please")[0].strip("\n")
    txt_path = os.path.join(cwd, day_number, f"{day_number}.txt")
    with open(txt_path, "w+") as file:
        file.write(parsed_response)

    # get example answer
    try:
        text = response.text
        regex = "<em><code>(.*?)</code></em>"
        answer = re.findall(regex, text, re.DOTALL)[-1]
        example_path = os.path.join(cwd, day_number, f"example_answer.txt")
        with open(example_path, "w+") as file:
            file.write(answer)
    except IndexError:
        try:
            regex = "<code><em>(.*?)</em></code>"
            answer = re.findall(regex, text, re.DOTALL)[-1]
            example_path = os.path.join(cwd, day_number, f"example_answer.txt")
            with open(example_path, "w+") as file:
                file.write(answer)
        except IndexError:
            print("Looks like there's something funky going on with the example answer")

    # get puzzle input
    if gh_cookie:
        response = requests.get(day_url + "/input", headers={"cookie": gh_cookie})
        parsed_response = str(response.text).strip("\n")
        input_path = example_path = os.path.join(cwd, day_number, f"input.txt")
        with open(input_path, "w+") as file:
            file.write(parsed_response)


def post_answer(day, answer, level=1, year=YEAR):
    year = year if year else YEAR
    day_url = BASE_URL + f"{year}/day/{str(day)}"
    gh_cookie = os.environ.get("GH_COOKIE")
    body = {"answer": str(answer), "level": level}
    response = requests.post(
        day_url + "/answer", data=body, headers={"cookie": gh_cookie}
    )
    print(response.text)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", action="store_true")
    parser.add_argument("-d", "--day", type=int, help="Day to pull down")
    parser.add_argument("-y", "--year", type=int, help="AoC year to target")
    args = parser.parse_args()
    if args.init:
        create_folder_structure()
    if args.day:
        download_problem_for_day(args.day, year=args.year)
