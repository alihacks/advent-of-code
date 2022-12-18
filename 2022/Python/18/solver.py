from typing import List
import itertools


def neighbors(x, y, z):
    return [(x+dx, y+dy, z+dz) for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]]

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 64
        self.test2 = 58


    def parse(self, instr: str) -> List:
        self.N = 0
        self.data = set()
        for x,y,z in [map(int,line.split(',')) for line in instr.splitlines()]:
            self.N = max(self.N, x,y,z)
            self.data.add((x,y,z))

    def is_trapped(self, x, y, z):
        queue = [(x,y,z)]
        seen = set()
        
        while queue:
            x, y, z = queue.pop()
            seen.add((x, y, z))
            if (x,y,z) in self.data:
                continue
            if min(x, y, z) < 0 or max(x, y, z) >= self.N: # reach edge
                return False
            for xn, yn, zn in neighbors(x, y, z):
                if (xn, yn, zn) in self.trapped: # you're trapped if your neighbor is
                    return True
                if (xn, yn, zn) not in seen:
                    seen.add((xn, yn, zn))
                    queue.append((xn, yn, zn))
        return True


    def solve(self):
        self.trapped = set()
        for x,y,z in itertools.product(range(self.N),range(self.N),range(self.N)):
            if (x,y,z) not in self.data and  self.is_trapped(x, y, z):
                self.trapped.add((x, y, z))

        for x,y,z in self.data:
            for neighbor in neighbors(x,y,z):
                if neighbor not in self.data:
                    self.part1 += 1
                    if neighbor not in self.trapped:
                        self.part2 += 1