from typing import List
import heapq
from collections import defaultdict
import itertools 

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 1
        self.test2 = 285

    def parse(self, instr: str) -> List:
        g = [list(line) for line in instr.splitlines()]
        self.R = len(g)
        self.C = len(g[0])
        self.g = set()
        for r in range(self.R):
            for c in range(self.C):
                if g[r][c] == '#': continue
                if g[r][c] == 'S':
                    self.start = (r,c)
                elif g[r][c] == 'E':
                    self.end = (r,c)
                self.g.add((r,c))

    def solve(self):
        moves = [(-1,0),(0,1),(1,0),(0,-1)]
        def search():
            q = [(0,*self.start)]
            dist = {}
            while q:
                d,r,c = heapq.heappop(q)
                if (r,c) in dist: continue
                dist[(r,c)] = d
                for dr, dc in moves:
                    rr,cc = r+dr,c+dc
                    if (rr,cc) in self.g:
                        heapq.heappush(q, (d+1, rr,cc))
            return dist
        
        def count_cheats(limit = 2):
            m2 = []
            for dr, dc in itertools.product(range(-limit, limit + 1), repeat=2):
                if 1 < abs(dr) + abs(dc) <= limit:
                    m2.append((dr, dc))
            cheats = set()
            for r,c in dist:
                for dr, dc in m2:
                    rr, cc = r + dr, c + dc
                    if (rr,cc) in dist:
                        gain = dist[(rr,cc)] - dist[(r,c)] - (abs(dr) + abs(dc))
                        if gain >= (50 if self.is_test else 100):
                            cheats.add((r,c,rr,cc))
            return len(cheats)

        dist = search()
        self.part1 = count_cheats()
        self.part2 = count_cheats(20)
