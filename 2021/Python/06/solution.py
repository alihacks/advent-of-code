from typing import List
from collections import defaultdict


def parse(instr: str) -> List:
    return [int(num) for num in instr.split(",")]


def give_birth(start_list: List, day_count: int) -> int:
    delta = 7  # takes 6 days to give birth, so new one appears on day 7
    delta0 = 9  # except 8 days on first time
    births = defaultdict(lambda: 0)
    population = len(start_list)
    for d in start_list:
        births[d + 1] += 1

    for day in range(1, day_count + 1):
        birth_count = births[day]
        if birth_count > 0:
            population = population + birth_count
            births[day + delta] += birth_count
            births[day + delta0] += birth_count
    return population


def partOne(instr: str) -> int:
    return give_birth(parse(instr), 80)


def partTwo(instr: str) -> int:
    return give_birth(parse(instr), 256)
