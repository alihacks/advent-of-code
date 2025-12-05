from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 357
        self.test2 = 3121910778619

    def parse(self, instr: str) -> List:
        self.data = [list(map(int,line)) for line in instr.strip().splitlines()]

    def solve(self):

        def maxbatt(bank, n):
            res = ''
            si = 0
            for i in range(0,n):
                ei = len(bank) - (n - i) + 1
                val = max(bank[si:ei])
                index = bank[si:ei].index(val)
                si = si + index + 1
                res += str(val)
            return int(res)

        for bank in self.data:
            self.part1 += maxbatt(bank,2)
            self.part2 += maxbatt(bank,12)
