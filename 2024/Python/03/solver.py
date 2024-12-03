from typing import List
import re
from operator import mul
from functools import reduce


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 161
        self.test2 = 48

    def parse(self, instr: str) -> List:
        self.data = instr

    def solve(self):
        mulex = r'mul\([0-9]+\,[0-9]+\)'
        parts = re.findall( mulex, self.data)
        def mulit(part):
            return reduce(mul,map(int,part[4:-1].split(',')))

        for part in parts:
            self.part1 += mulit(part)
        
        parts = re.findall(r'do\(\)|don\'t\(\)|' + mulex, self.data)
        doit = True
        for part in parts:
            if part == 'do()':
                doit = True
            elif part == "don't()":
                doit = False
            elif doit:
                self.part2 += mulit(part)
