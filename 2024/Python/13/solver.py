from typing import List
import re
import numpy as np  
from scipy.optimize import minimize, LinearConstraint  
import pulp

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 480
        self.test2 = 875318608908

    def parse(self, instr: str) -> List:
        self.data = [tuple(map(int, re.findall(r'\d+', game))) for game in instr.split('\n\n')]

    def solve(self):
        # had to resort to math for p2, kept for p1 too
        def compute(ax, ay, bx, by, px, py):
            b, bm = divmod(py * ax - px * ay, by * ax - bx * ay)
            a, am = divmod((px - b * bx), ax)
            return 0 if bm or am or a < 0 or b < 0 else 3*a + b

        for ax, ay, bx, by, px, py in self.data:
            self.part1 += compute(ax, ay, bx, by, px, py)
            self.part2 += compute(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
