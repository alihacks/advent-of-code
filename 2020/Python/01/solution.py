from typing import List


def parse(instr: str) -> List:
    return [
        int(line)
        for line in instr.splitlines()
    ]


def partOne(instr: str) -> int:
    input_list = parse(instr)
    for i in input_list:
        for j in input_list:
            if i + j == 2020:
                return i * j
    return 0


def partTwo(instr: str) -> int:
    input_list = parse(instr)
    for i in input_list:
        for j in input_list:
            for k in input_list:
                if i + j + k == 2020:
                    return i * j * k
    return 0
