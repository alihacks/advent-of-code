from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 3
        self.test2 = 6

    def parse(self, instr: str) -> List:
        self.data = [int(line.replace('R','').replace('L','-')) for line in instr.strip().splitlines()]

    def solve(self):
        n = 50
        for m in self.data:
            if m > 0 and n + m >=100:
                self.part2 += (n + m) // 100
            elif m < 0 and n + m <= 0:
                self.part2 += abs(m + n) // 100
                if n != 0: # Passed 0?
                    self.part2 += 1

            n = (n + m) % 100
            if n == 0:
                self.part1 += 1

