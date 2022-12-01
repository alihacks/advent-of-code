from typing import List


class Solver:
    def __init__(self, input, is_test: bool):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 24000
        self.test2 = 45000

    def parse(self, instr: str) -> List:
        self.data = [part.splitlines() for part in instr.split('\n\n')]

    def solve(self):
        calories = [sum([int(val) for val in elf]) for elf in self.data]

        self.part1 = max(calories)
        self.part2 = sum(sorted(calories, reverse=True)[:3])
