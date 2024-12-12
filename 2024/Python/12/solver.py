from typing import List
from collections import defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 1930
        self.test2 = 1206

    def parse(self, instr: str) -> List:
        g = [list(line) for line in instr.splitlines()]
        self.g = {}
        for r in range(len(g)):
            for c in range(len(g[0])):
                self.g[complex(r,c)] = g[r][c]

    def solve(self):
        D = [1, -1, 1j, -1j]
        def flood_fill(grid, rc, visited):  
            q = [rc]
            area = []

            while q:
                current = q.pop()
                if current in visited:
                    continue
                visited.add(current)
                area.append(current)
    
                for n in [current + d for d in D]:
                    if n in grid and grid[n] == grid[rc] and n not in visited:
                        q.append(n)  
            return area
        
        def find_areas(grid):  
            visited = set()  
            areas = []  
        
            for rc in grid:  
                if rc not in visited:  
                    area = flood_fill(grid, rc, visited)  
                    if area:  
                        areas.append(area)  
            return areas  

        for area in find_areas(self.g):
            fc = 0 
            fences = defaultdict(dict)
            for k in area:
                for d in D:
                    if (k + d) not in self.g or self.g[k + d] != self.g[k]:
                        fc += 1
                        fences[d][k+d] = 1

            self.part1 +=  fc * len(area)
            self.part2 +=  len(area) * sum([len(find_areas(f)) for _,f in fences.items()])