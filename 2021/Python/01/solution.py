from typing import List


def parse(instr: str) -> List:
    return [int(line) for line in instr.splitlines()]


def get_incs(list: List) -> int:
    prev = -1
    inc = 0
    for i in list:
        if prev >= 0 and i > prev:
            inc = inc + 1
        prev = i
    return inc


def partOne(instr: str) -> int:
    input_list = parse(instr)
    return get_incs(input_list)


def partTwo(instr: str) -> int:
    input_list = parse(instr)
    sums = []
    for i in range(2, len(input_list)):
        sums.append(input_list[i - 2] + input_list[i - 1] + input_list[i])
    return get_incs(sums)
