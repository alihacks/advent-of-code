from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 4890
        self.test2 = '2=-1=0'

    def parse(self, instr: str) -> List:
        self.data = [line for line in instr.splitlines()]

    def solve(self):
        def s_i(v):
            res = 0
            for i, digit in enumerate(str(v)[::-1]):
                digit = -1 if digit == '-' else \
                    -2 if digit == '=' else int(digit)
                res += 5 ** i * digit
            return res

        def i_s(v):
            digs = []
            while v > 0:
                digs.append(v % 5)
                v //= 5

            for i, d in enumerate(digs):
                if d == 3:
                    digs[i+1] += 1
                    digs[i] = '='
                elif d == 4:
                    digs[i+1] += 1
                    digs[i] = '-'
                elif d == 5:
                    digs[i+1] += 1
                    digs[i] = 0
            return ''.join([str(d) for d in digs[::-1]])

        self.part1 = sum(map(s_i, self.data))
        self.part2 = i_s(self.part1)
