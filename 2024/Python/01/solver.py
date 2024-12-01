from typing import List
from collections import Counter

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 11
        self.test2 = 31

    def parse(self, instr: str) -> List:
        self.data = [[int(i) for i in line.split()] for line in instr.splitlines()]

    def solve(self):
        self.part1 = 0
        l,r = map(sorted, map(list, zip(*self.data)))
        for (i, j) in zip(l, r):
            self.part1+= abs(i-j)

        counts = Counter(r)
        self.part2 = sum([i * counts[i] for i in l])
