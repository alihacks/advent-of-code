from typing import List


def parse(instr: str) -> List:
    return [int(line) for line in instr.splitlines()]


def get_incs(list: List) -> int:
    return sum(map(lambda i: 1 if list[i] > list[i - 1] else 0, range(1, len(list))))


def partOne(instr: str) -> int:
    input_list = parse(instr)
    return get_incs(input_list)


def partTwo(instr: str) -> int:
    input_list = parse(instr)
    sums = []
    for i in range(2, len(input_list)):
        sums.append(sum(input_list[i - 2 : i + 1]))
    return get_incs(sums)
