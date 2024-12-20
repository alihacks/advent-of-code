from typing import List
from functools import cache

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 6
        self.test2 = 16

    def parse(self, instr: str) -> List:
        instr = instr.splitlines()
        self.towels = instr[0].split(', ')
        self.str = instr[2:]

    def solve(self):
        @cache
        def fit(s):
            return 1 if s == '' else sum([fit(s[len(towel):]) for towel in self.towels if s.startswith(towel)])

        self.part1 = sum([fit(s) > 0 for s in self.str])
        self.part2 = sum([fit(s) for s in self.str])

