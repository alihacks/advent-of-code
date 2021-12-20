from typing import List


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 35
        self.test2 = 3351
        self.part2 = 0

    def parse(self, instr) -> List:
        self.grid = set()
        self.lookup = set()
        lines = instr.splitlines()
        for i in range(len(lines[0])):
            if lines[0][i] == "#":
                self.lookup.add(i)
        self.R = len(lines) - 2
        self.C = len(lines[2])
        for r in range(2, len(lines)):
            line = lines[r]
            for c in range(len(line)):
                if line[c] == "#":
                    self.grid.add((r - 2, c))
        self.flipped = False
        self.is_flipper = 0 in self.lookup

    def get_val(self, r, c):
        lk, i = 0, 8
        for ri in range(r - 1, r + 2):
            for ci in range(c - 1, c + 2):
                if self.flipped == ((ri, ci) not in self.grid):
                    lk += 2 ** i
                i -= 1
        return lk

    def solve(self):

        for i in range(50):
            next_grid = set()
            for ri in range(-1 * (i + 1), self.R + 2):
                for ci in range(-1 * (i + 1), self.C + 2):
                    nv = self.get_val(ri, ci)
                    if self.is_flipper and self.flipped == (nv in self.lookup):
                        next_grid.add((ri, ci))
                    elif not self.is_flipper and nv in self.lookup:
                        next_grid.add((ri, ci))
            self.R += 2
            self.C += 2
            self.grid = next_grid
            if self.is_flipper:
                self.flipped = not self.flipped
            if i + 1 == 2:
                self.part1 = len(next_grid)
            elif i + 1 == 50:
                self.part2 = len(next_grid)
