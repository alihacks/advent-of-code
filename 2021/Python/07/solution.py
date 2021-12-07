from typing import List


def parse(instr: str) -> List:
    return [int(num) for num in instr.split(",")]


def partOne(instr: str) -> int:
    nums = parse(instr)
    sums = []
    for i in range(min(nums), max(nums) + 1):
        s = sum([abs(n - i) for n in nums])
        sums.append(s)
    return min(sums)


def partTwo(instr: str) -> int:
    nums = parse(instr)
    sums = []
    for i in range(min(nums), max(nums) + 1):
        s = sum([abs(n - i) * (abs(n - i) + 1) // 2 for n in nums])
        sums.append(s)
    return min(sums)
