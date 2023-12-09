from typing import List
from itertools import pairwise

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 114
        self.test2 = 2

    def parse(self, instr: str) -> List:
        self.data = [[int(i) for i in line.split()] for line in instr.splitlines()]

    def solve(self):
        self.part1 = 0

        def steps(seq):
            if set(seq) == {0}:
                return 0
            return steps([b - a for a, b in pairwise(seq)]) + seq[-1]

        self.part1 = sum(steps(l) for l in self.data)
        self.part2 = sum(steps(l[::-1]) for l in self.data)
