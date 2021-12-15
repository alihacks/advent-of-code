from typing import List


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 0
        self.test2 = 0
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr) -> List:
        self.data = [list(line) for line in instr.splitlines()]

    def solve(self):
        self.part1 = 0
