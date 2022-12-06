from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 7
        self.test2 = 19
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = instr.strip()

    def find(self, n):
        for i in range(len(self.data)-n):
            if len(set(self.data[i:i+n])) == n:
                return i + n

    def solve(self):
        self.part1 = self.find(4)
        self.part2 = self.find(14)
