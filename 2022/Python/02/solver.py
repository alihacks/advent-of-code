from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 15
        self.test2 = 12
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [line.replace(' ', '') for line in instr.splitlines()]

    def solve(self):
        scores = {'AX': 1 + 3,
                  'BX': 1 + 0,
                  'CX': 1 + 6,
                  'AY': 2 + 6,
                  'BY': 2 + 3,
                  'CY': 2 + 0,
                  'AZ': 3 + 0,
                  'BZ': 3 + 6,
                  'CZ': 3 + 3}
        self.part1 = sum([scores[game] for game in self.data])

        scores = {'AX': 3,
                  'BX': 1,
                  'CX': 2,
                  'AY': 3 + 1,
                  'BY': 3 + 2,
                  'CY': 3 + 3,
                  'AZ': 6 + 2,
                  'BZ': 6 + 3,
                  'CZ': 6 + 1}

        self.part2 = sum([scores[game] for game in self.data])
