from typing import List
import re


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 4277556
        self.test2 = 3263827

    def parse(self, instr: str) -> List:
        g = [re.split('\s+', line.strip()) for line in instr.splitlines()]
        self.g = [list(line) for line in instr.splitlines()[0:-1]]
        self.data = [list(map(int,n)) for n in g[:-1]]
        self.ops = g[-1]

    def solve(self):
        for i in range(len(self.ops)):
            op = self.ops[i]
            r = 0 if op == '+' else 1
            for val in self.data:
                if op == '+':
                    r += val[i]
                else:
                    r *= val[i]
            self.part1 += r

        rev = self.g[::-1]
        g = [''.join(list(col)[::-1]).strip() for col in zip(*rev)][::-1]
        n = 0
        for i in range(len(self.ops)):
            op = self.ops[::-1][i]
            r = 0 if op == '+' else 1
            while True:
                val = int(g[n])
                #print(val, op)
                if op == '+':
                    r += val
                else:
                    r *= val
                n += 1
                if n >= len(g) or g[n] == '':
                    n += 1
                    break
            self.part2 += r

