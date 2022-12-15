from typing import List
import re

def md(x,y,x1,y1):
    return abs(x-x1) + abs(y-y1)

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 26
        self.test2 = 56000011

    def parse(self, instr: str) -> List:
        self.data = []
        self.md = []
        for x,y,xb,yb in [map(int,re.findall(r'\-?\d+',line)) for line in instr.splitlines()]:
            self.data.append((x,y,xb,yb))
            self.md.append(md(x,y,xb,yb))

    def solve(self):
        x_min = min([d[0] for d in self.data]) - max(self.md)
        x_max = max([d[0] for d in self.data]) + max(self.md)

        Y = 10 if self.is_test else 2000000
        x = x_min
        while x <= x_max:
            for i, d in enumerate(self.data):
                xs, ys, _, _ = d
                dist_diff = self.md[i] - md(xs,ys,x,Y)
                if dist_diff >= 0:
                    self.part1 += dist_diff + 1
                    x += dist_diff
                    break
            x += 1
        self.part1 -= len(set([d[2] for d in self.data if d[3] == Y]))

        beacons = set([(d[2],d[3]) for d in self.data])
        stop = 20 if self.is_test else 4000000
        for y in range(stop):
            x = 0
            while x < stop:
                is_full = False
                for i, d in enumerate(self.data):
                    xs, ys, _, _ = d
                    dist_diff = self.md[i] - md(xs,ys,x,y)
                    if dist_diff >= 0:
                        x += dist_diff
                        is_full = True
                        break
                if not is_full and (x,y) not in beacons:
                    self.part2 = x * 4000000 + y
                    return
                x += 1
        
