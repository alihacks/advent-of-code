from typing import List


def parse(instr: str) -> List:
    return [
        line
        for line in instr.splitlines()
    ]


def go_sled(grid, x_delta, y_delta) -> int:
    cnt = 0
    x, y = 0, 0
    x_max, y_max = len(grid[0]), len(grid)
    while y < y_max:
        if (grid[y][x % x_max] == '#'):
            cnt += 1
        x += x_delta
        y += y_delta
    return cnt


def partOne(instr: str) -> int:
    input_list = parse(instr)
    return go_sled(input_list, 3, 1)


def partTwo(instr: str) -> int:
    input_list = parse(instr)
    cnt = 1
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    for x, y in slopes:
        cnt *= go_sled(input_list, x, y)
    return cnt
