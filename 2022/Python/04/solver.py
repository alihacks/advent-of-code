from typing import List
import re


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 2
        self.test2 = 4
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [list(map(int, re.split(r',|-', line)))
                     for line in instr.splitlines()]

    def solve(self):
        for x0, x1, y0, y1 in self.data:
            r1 = set(range(x0, x1+1))
            r2 = set(range(y0, y1+1))
            if r1.issubset(r2) or r2.issubset(r1):
                self.part1 += 1
            if r1.intersection(r2):
                self.part2 += 1
