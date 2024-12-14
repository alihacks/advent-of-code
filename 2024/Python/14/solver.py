from typing import List
import re
from collections import defaultdict
from functools import reduce
from operator import mul


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 12, 0
        self.test1 = 12
        self.test2 = 0

    def parse(self, instr: str) -> List:
        self.X = 11 if self.is_test else 101
        self.Y = 7 if self.is_test else 103
        self.data = [tuple(map(int, re.findall(r'\-?\d+', game))) for game in instr.splitlines()]

    def solve(self):
        def flood_fill(grid, rc, visited):
            q = [rc]
            ac = 0
            while q:
                current = q.pop()
                if current in visited: continue
                visited.add(current)
                ac += 1
                for n in [current + d for d in [1, -1, 1j, -1j]]:
                    if n in grid and n not in visited:
                        q.append(n)
            return ac
        
        def count_areas(grid, min_size = 2):
            visited = set()
            ac = 0
            for rc in grid:
                if rc not in visited:
                    area = flood_fill(grid, rc, visited)
                    if area >= min_size:
                        ac += 1
            return ac
        
        def arrange(n, p2 = False):
            g = set() if p2 else defaultdict(int)
            for x,y,vx,vy in self.data:
                x1 = (x + n * vx) % self.X
                y1 = (y + n * vy) % self.Y
                if p2:
                    g.add(complex(x1,y1))
                else: 
                    g[(x1,y1)] += 1
            return g
        
        mx, my = self.X // 2, self.Y // 2
        quadrants = defaultdict(int)
        pos = arrange(100)
        for x,y in pos:
            if x != mx and y != my:
                quadrants[x < mx, y < my] += pos[(x,y)]
            
        self.part1 = reduce(mul, quadrants.values())
        if self.is_test: return
        for i in range(10000):
            g = arrange(i, True)
            ac = count_areas(g)
            if ac < 10:
                print(ac)
                self.part2 = i
                for y in range(self.Y):
                    for x in range(self.X):
                        print("#" if complex(x,y) in g else ' ', end='')
                    print()
                break
