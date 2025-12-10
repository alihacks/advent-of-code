from typing import List
from shapely.geometry import Polygon, box
from shapely.prepared import prep
import itertools

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 50
        self.test2 = 24

    def parse(self, instr: str) -> List:
        self.data = [tuple(map(int,line.split(','))) for line in instr.splitlines()]

    def solve(self):
        a = [r+c for r,c in self.data]
        b = [r-c for r,c in self.data]
        a0 = self.data[a.index(min(a))]
        a1 = self.data[a.index(max(a))]
        b0 = self.data[b.index(min(b))]
        b1 = self.data[b.index(max(b))]

        def area(c1, c2):
            x1, y1 = c1
            x2, y2 = c2
            return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        aa = area(a0,a1)
        ba = area(b0,b1)
        self.part1 = max(aa,ba)

        outline = prep(Polygon(self.data))
        for c1, c2 in itertools.combinations(self.data,2):
            x1, y1 = c1
            x2, y2 = c2
            rect = box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            a = area(c1, c2)
            if outline.contains(rect) and a > self.part2:
                self.part2 = a
