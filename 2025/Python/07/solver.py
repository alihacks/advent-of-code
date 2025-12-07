from typing import List
from collections import defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 21
        self.test2 = 40

    def parse(self, instr: str) -> List:
        self.data = [line for line in instr.splitlines()]
        self.s = self.data[0].index('S')

    def solve(self):
        curr = set([(1,self.s)])
        beams = curr.copy()
        for n in range(1,len(self.data) - 1):
            next = set()
            for (r,c) in curr:
                if self.data[r+1][c] == '.':
                    next.add((r+1,c))
                elif self.data[r+1][c] == '^':
                    next.add((r+1,c-1))
                    next.add((r+1,c+1))
                    self.part1 += 1
            beams.update(next)
            curr = next

        paths = {}

        def count_paths(r,c):
            if r == len(self.data):
                return 1
            if (r,c) not in paths:
                if self.data[r][c] == '^':
                    paths[(r,c)] = count_paths(r+1,c-1) + count_paths(r+1,c+1)
                else:
                    paths[(r,c)] = count_paths(r+1,c)
            return paths[(r,c)]

        self.part2 = count_paths(1, self.s)
