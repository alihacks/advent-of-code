from typing import List
from collections import defaultdict
from itertools import permutations

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 14
        self.test2 = 34

    def parse(self, instr: str) -> List:
        g = [list(line) for line in instr.splitlines()]
        self.R = len(g)
        self.C = len(g[0])
        self.antennas = defaultdict(set)
        for r in range(self.R):
            for c in range(self.C):
                if g[r][c] != '.':
                    self.antennas[g[r][c]].add(complex(r,c))

    def solve(self):
        def in_grid(rc):
            return 0 <= rc.real < self.R and 0 <= rc.imag < self.C

        def count(p2 = False):
            antinodes = set()
            for _, coords in self.antennas.items():
                if p2:
                    antinodes.update(coords)
                for a, b in permutations(coords, 2):
                    d = b - a
                    loc = b + d
                    while in_grid(loc):
                        antinodes.add(loc)
                        if not p2:
                            break
                        loc += d
            return len(antinodes)

        self.part1 = count()
        self.part2 = count(True)
