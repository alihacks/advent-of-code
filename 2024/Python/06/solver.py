from typing import List
from collections import defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 41
        self.test2 = 6

    def parse(self, instr: str) -> List:
        g = [list(line) for line in instr.splitlines()]
        self.R = len(g)
        self.C = len(g[0])
        self.obs = set()
        for r in range(self.R):
            for c in range(self.C):
                if g[r][c] == '#':
                    self.obs.add(complex(r,c))
                elif g[r][c] == '^':
                    self.guard = complex(r,c)

    def solve(self):
        vectors = [-1+0j,0+1j,1+0j,0-1j] # U, R, D, L
        
        def walk(extra = -1):
            g = self.guard
            vi = 0
            visits = defaultdict(set)
            visits[g].add(vi)
            while True:
                g1 = g + vectors[vi]
                if  g1.real < 0 or g1.real >= self.R or g1.imag < 0 or g1.imag >=self.C:
                    break
                if g1 == extra or g1 in self.obs:
                    vi = (vi + 1) % 4
                else:
                    if vi in visits[g1]:
                        return False
                    visits[g1].add(vi)
                    g = g1
            return visits
        
        visits = walk()
        self.part1 = len(visits)

        for pos in visits:
            if not walk(pos):
                self.part2 += 1
