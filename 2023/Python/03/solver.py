from typing import List
from collections import defaultdict
import re, math


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 4361
        self.test2 = 467835

    def parse(self, input_string) -> List:
        self.grid = []
        for line in input_string.splitlines():
            self.grid.append(line)
        self.R = len(self.grid)
        self.C = len(self.grid[0])

    def get_neighbors(self, r, c):
        n = []
        adj = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
        for dr, dc in adj:
            rr, cc = r + dr, c + dc
            if 0 <= rr < self.R and 0 <= cc < self.C:
                val = self.grid[rr][cc]
                if val != "." and not val.isdigit():
                    n.append((val, rr, cc))
        return n
    
    def has_symbol(self, r, c):
        return len(self.get_neighbors(r,c)) > 0
    
    def get_gear(self, r, c):
         for n in self.get_neighbors(r,c):
            if n[0] == '*':
                return (n[1], n[2])

    def solve(self):
        self.part1 = 0
        gears = defaultdict(list)
        for r in range(self.R):
            iter = re.finditer(r'\d+', self.grid[r])
            for m in iter:
                num = int(m[0])
                is_part = False
                for col in range(m.start(0), m.end(0)):
                    if self.has_symbol(r,col):
                        is_part = True
                        gear = self.get_gear(r,col)
                        if gear:
                            gears[gear].append(num)
                            break
                if is_part:
                    self.part1 += num

        self.part2 = sum(math.prod(vals) for vals in gears.values() if len(vals) == 2)
        