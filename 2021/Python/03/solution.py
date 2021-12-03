from typing import List
from collections import Counter


def parse(instr: str) -> List:
    return [line for line in instr.splitlines()]


def partOne(instr: str) -> int:
    nums = parse(instr)
    maxlen = len(max(nums, key=len))
    counters = [Counter() for i in range(maxlen)]
    for num in nums:
        for i, v in enumerate(num):
            counters[i].update(v)
    gamma, epsilon = "", ""
    for c in counters:
        if c["0"] > c["1"]:
            gamma = gamma + "0"
            epsilon = epsilon + "1"
        else:
            gamma = gamma + "1"
            epsilon = epsilon + "0"
    return int(gamma, 2) * int(epsilon, 2)


def find_bit_criteria(nums: list, i: int, is_co2: bool):
    counter = Counter()
    for num in nums:
        counter.update(num[i])
    c0, c1 = counter["0"], counter["1"]
    if not is_co2:
        return "1" if c1 >= c0 else "0"
    else:
        return "0" if c0 <= c1 else "1"


def eliminate_nums(nums: list, i: int, criteria: str) -> list:
    return [n for n in nums if n[i] == criteria]


def partTwo(instr: str) -> int:
    nums = parse(instr)
    maxlen = len(max(nums, key=len))
    res = 1
    for is_co2 in [False, True]:
        new_list = nums.copy()
        for i in range(maxlen):
            criteria = find_bit_criteria(new_list, i, is_co2)
            new_list = eliminate_nums(new_list, i, criteria)
            if len(new_list) == 1:
                break
        res = res * int(new_list[0], 2)
    return res
