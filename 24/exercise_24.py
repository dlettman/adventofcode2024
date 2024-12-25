import time

import pyperclip

from helpers import helpers

from collections import defaultdict
from itertools import combinations, permutations


class AndGate(object):
    def __init__(self, a, b, output):
        self.a = a
        self.b = b
        self.output = output
        self.done = False

    def charge(self, a, b):
        if a is None or b is None:
            return None
        if a == 1 and b == 1:
            return 1
        else:
            return 0


class OrGate(object):
    def __init__(self, a, b, output):
        self.a = a
        self.b = b
        self.output = output
        self.done = False

    def charge(self, a, b):
        if a is None or b is None:
            return None
        if a == 1 or b == 1:
            return 1
        else:
            return 0


class XorGate(object):
    def __init__(self, a, b, output):
        self.a = a
        self.b = b
        self.output = output
        self.done = False

    def charge(self, a, b):
        if a is None or b is None:
            return None
        if (a == 1 and b == 0) or (b == 1 and a == 0):
            return 1
        else:
            return 0


def get_wires_and_gates(puzzle_input):
    wires, gates = puzzle_input.split("\n\n")
    wire_dict = dict()
    gate_list = []
    for wire in wires.splitlines():
        print(wire)
        wire, charge = wire.split(": ")
        wire_dict[wire] = int(charge)
    for gate in gates.splitlines():
        a, operator, b, _, output = gate.split(" ")
        if operator == "AND":
            gate_list.append(AndGate(a, b, output))
        elif operator == "OR":
            gate_list.append(OrGate(a, b, output))
        elif operator == "XOR":
            gate_list.append(XorGate(a, b, output))
    return wire_dict, gate_list


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename, split=False)
    wire_dict, gate_list = get_wires_and_gates(puzzle_input)
    lit_one_up = True
    while lit_one_up:
        lit_one_up = False
        for gate in gate_list:
            if gate.output not in wire_dict:
                wire_dict[gate.output] = None
            if not gate.done:
                if gate.a not in wire_dict:
                    wire_dict[gate.a] = None
                if gate.b not in wire_dict:
                    wire_dict[gate.b] = None
                if wire_dict[gate.a] is not None and wire_dict[gate.b] is not None:
                    lit_one_up = True
                    wire_dict[gate.output] = gate.charge(
                        wire_dict[gate.a], wire_dict[gate.b]
                    )
                    gate.done = True
    z_gates = sorted(
        [(wire, charge) for wire, charge in wire_dict.items() if wire.startswith("z")]
    )[::-1]
    bin = int("".join([str(item[1]) for item in z_gates]), 2)
    print("woof")
    return bin


def part_two(input_filename):
    """
    I ended up doing a lot of this by hand / manually, so the code doesn't really tell the whole story
    """
    puzzle_input = helpers.parse_input(input_filename, split=False)
    wire_dict, gate_list = get_wires_and_gates(puzzle_input)
    gate_dict = {gate.output: gate for gate in gate_list}
    x_wires = sorted(
        [(wire, charge) for wire, charge in wire_dict.items() if wire.startswith("x")]
    )[::-1]
    x_bin = int("".join([str(item[1]) for item in x_wires]), 2)
    print(f"x_bin = ", x_bin)

    y_wires = sorted(
        [(wire, charge) for wire, charge in wire_dict.items() if wire.startswith("y")]
    )[::-1]
    y_bin = int("".join([str(item[1]) for item in y_wires]), 2)
    print(f"y_bin = ", y_bin)
    lit_one_up = True
    while lit_one_up:
        lit_one_up = False
        for gate in gate_list:
            if gate.output not in wire_dict:
                wire_dict[gate.output] = None
            if not gate.done:
                if gate.a not in wire_dict:
                    wire_dict[gate.a] = None
                if gate.b not in wire_dict:
                    wire_dict[gate.b] = None
                if wire_dict[gate.a] is not None and wire_dict[gate.b] is not None:
                    lit_one_up = True
                    wire_dict[gate.output] = gate.charge(
                        wire_dict[gate.a], wire_dict[gate.b]
                    )
                    gate.done = True
    for gate in gate_list:
        if gate.output.startswith("z"):
            if not isinstance(gate, XorGate):
                print(f"!!! {gate.output} is not an XOR")
        else:
            if not (
                (gate.a.startswith("x") and gate.b.startswith("y"))
                or (gate.a.startswith("y") and gate.b.startswith("x"))
            ):
                if isinstance(gate, XorGate):
                    print(f"!!! {gate.output} is an XOR but shouldn't be")
    for gate in gate_list:
        if gate.output == "z45":
            print(
                f"z45: output: {gate.output}, a: {gate.a}, b: {gate.b}. Type = {type(gate)}"
            )
    xor_gates = [gate for gate in gate_list if isinstance(gate, XorGate)]
    for xor_gate in xor_gates:
        if (xor_gate.a.startswith("x") and xor_gate.b.startswith("y")) or (
            xor_gate.a.startswith("y") and xor_gate.b.startswith("x")
        ):
            found_a_match = False
            for xor_gate2 in xor_gates:
                if xor_gate2.a == xor_gate.output or xor_gate2.b == xor_gate.output:
                    found_a_match = True
                    break
            if not found_a_match:
                print(
                    f"!!! {xor_gate.output} doesn't input to another XOR. Inputs = {xor_gate.a}, {xor_gate.b}"
                )

    and_gates = [gate for gate in gate_list if isinstance(gate, AndGate)]
    or_gates = [gate for gate in gate_list if isinstance(gate, OrGate)]

    for and_gate in and_gates:
        if (gate.a.startswith("x") and gate.b.startswith("y")) or (
            gate.a.startswith("y") and gate.b.startswith("x")
        ):
            found_a_match = False
            for or_gate in or_gates:
                if (or_gate.a == and_gate.output) or (or_gate.b == and_gate.output):
                    found_a_match = True
                    break
            if not found_a_match:
                print(
                    f"!!! {and_gate.output} doesn't input to an OR. Inputs = {and_gate.a}, {and_gate.b}"
                )

            z_gates = sorted(
                [
                    (wire, charge)
                    for wire, charge in wire_dict.items()
                    if wire.startswith("z")
                ]
            )[::-1]
    z_gates = sorted(
        [(wire, charge) for wire, charge in wire_dict.items() if wire.startswith("z")]
    )[::-1]

    z_bin = int("".join([str(item[1]) for item in z_gates]), 2)
    off_by = abs((x_bin + y_bin) - z_bin)
    print(f"Off by {off_by}")
    print("{0:b}".format(off_by))
    print("woof")
    return bin


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
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
