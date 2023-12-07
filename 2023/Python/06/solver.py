from typing import List
import re, math
from sympy import symbols, solve_univariate_inequality, S



class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 288
        self.test2 = 71503

    def parse(self, instr: str) -> List:
        times, dist = [[int(i) for i in re.findall(r"\d+",line)] for line in instr.splitlines()]
        self.data = zip(times, dist)
        self.data2 = [int(re.findall(r"\d+",line.replace(" ",""))[0]) for line in instr.splitlines()]
        
    def solve(self):
        self.part1 = 1

        def wins(time, dist):
            return len([n for n in range(time) if (time - n) * n > dist])
        
        def wins2(time, dist):
            n = symbols('n')
            return len(solve_univariate_inequality((time - n) * n > dist, n, relational=False).intersect(S.Integers))

        for time, dist in self.data:
            self.part1 *= wins2(time,dist)

        time, dist = self.data2
        self.part2 = wins2(time,dist)
