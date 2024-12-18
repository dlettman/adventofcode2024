import time

import pyperclip

from helpers import helpers

from math import trunc

import re


class Compooper(object):

    def __init__(self, a, b, c, program):
        self.pointer = 0
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.output = []
        self.opcode_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def combo(self, operand: int):
        if operand in (0, 1, 2, 3):
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            raise Exception("Invalid combo operand: ", operand)

    def adv(self, combo):  # 0
        numerator = self.a
        denominator = 2 ** (self.combo(combo))
        quotient = numerator / denominator
        self.a = trunc(quotient)
        # print(f"adv {numerator} by {denominator} (2^combo) {combo} = (truncated) {trunc(quotient)}")
        self.pointer += 2

    def bxl(self, literal):  # 1
        self.b = self.b ^ literal
        self.pointer += 2

    def bst(self, combo):  # 2
        self.b = self.combo(combo) % 8
        self.pointer += 2

    def jnz(self, literal):  # 3
        if self.a == 0:
            self.pointer += 2
        else:
            self.pointer = literal

    def bxc(self, _):  # 4
        self.b = self.b ^ self.c
        self.pointer += 2

    def out(self, combo):  # 5
        self.output.append(str(self.combo(combo) % 8))
        self.pointer += 2

    def bdv(self, combo):  # 6
        numerator = self.a
        denominator = 2 ** (self.combo(combo))
        quotient = numerator / denominator
        self.b = trunc(quotient)
        # print(f"bdv {numerator} by {denominator} (2^combo) {combo} = (truncated) {trunc(quotient)}")
        self.pointer += 2

    def cdv(self, combo):  # 7
        numerator = self.a
        denominator = 2 ** (self.combo(combo))
        quotient = numerator / denominator
        self.c = trunc(quotient)
        # print(f"cdv {numerator} by {denominator} (2^combo) {combo} = (truncated) {trunc(quotient)}")
        self.pointer += 2

    def execute(self):
        try:
            while True:
                # print(f"Pointer = {self.pointer}, Registers = a {self.a}, b {self.b}, c {self.c}")
                instruction = self.program[self.pointer]
                operand = self.program[self.pointer + 1]
                # print(f"executing instruction {instruction} with operand {operand}")
                self.opcode_map[instruction](operand)
        except IndexError:
            return ",".join([str(item) for item in self.output])


def get_program_and_registers(puzzle_input):
    registers, program = puzzle_input.split("\n\n")
    num_pattern = ".*: ([0-9]+)"
    a, b, c = [
        int(re.search(num_pattern, register).groups()[0])
        for register in registers.split("\n")
    ]
    program = [int(item) for item in program.split(": ")[1].split(",")]
    return a, b, c, program


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    a, b, c, program = get_program_and_registers(puzzle_input)
    print(a, b, c, program)
    compooper = Compooper(a, b, c, program)
    output = compooper.execute()
    return output


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    a, b, c, program = get_program_and_registers(puzzle_input)
    # print(a, b, c, program)

    # n = 181441
    # 181441 = [0, 3, 2, 4, 5, 0] - very close!

    # for n in range (1000000, 10000000):
    n = int(
        "".join(
            [
                "100",
                "000",
                "000",
                "000",
                "000",
                "000",
                "000",
                "111",
                "000",
                "111",
                "000",
                "111",
                "100",
                "110",
                "010",
                "010",
            ]
        ),
        2,
    )
    compooper = Compooper(n, b, c, program)
    output = compooper.execute()
    # print(program)
    output = [int(item) for item in output.split(",")]
    # print(n)
    print(f"OUTPUT = {output}")
    print(f"PROGRAM = {program}")
    if output == program:
        print("!!! DAMN !!!")
        return n
    elif len(output) < len(program):
        print("TOO SHORT! NUMBER MORE BIG!")
    elif len(output) > len(program):
        print("TOO LONG! NUMBER MORE SMALL!")
    else:
        print("RIGHT BALLPARK!")
    return


if __name__ == "__main__":
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # onestart = time.time()
    # p1result = part_one("input.txt")
    # oneend = time.time()
    # print(f"REAL RESULT = {p1result}")
    # print(f"Time = {oneend - onestart}")
    # print("\n")
    print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
