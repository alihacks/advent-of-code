from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 0
        self.test2 = 0

    def parse(self, instr: str) -> List:
        self.data = [list(line) for line in instr.splitlines()]

    def solve(self):
        print(self.data)
