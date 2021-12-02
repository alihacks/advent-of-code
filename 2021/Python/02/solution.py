from typing import List


def parse(instr: str) -> List:
    return [line for line in instr.splitlines()]


def partOne(instr: str) -> int:
    horizontal, depth = 0, 0
    for line in parse(instr):
        dir, amount = line.split(" ")
        amount = int(amount)
        if dir == "up":
            depth = depth - amount
        elif dir == "down":
            depth = depth + amount
        elif dir == "forward":
            horizontal = horizontal + amount
    return horizontal * depth


def partTwo(instr: str) -> int:
    horizontal, depth, aim = 0, 0, 0
    for line in parse(instr):
        dir, amount = line.split(" ")
        amount = int(amount)
        if dir == "up":
            aim = aim - amount
        elif dir == "down":
            aim = aim + amount
        elif dir == "forward":
            horizontal = horizontal + amount
            depth = depth + aim * amount

    return horizontal * depth
