from typing import List
import heapq

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 22
        self.test2 = '6,1'

    def parse(self, instr: str) -> List:
        self.data = [list(map(int,line.split(','))) for line in instr.splitlines()]
        self.max = 6 if self.is_test else 70

    def solve(self):
        g = set()
        p1stop = 12 if self.is_test else 1024
        for i in range(p1stop):
            g.add(tuple(self.data[i]))
        
        def search():
            moves = [(-1,0),(0,1),(1,0),(0,-1)]
            q = [(0,0,0)]
            dist = {}
            while q:
                d,r,c = heapq.heappop(q)
                if (r,c) in dist: continue
                dist[(r,c)] = d
                for dr, dc in moves:
                    rr,cc = r+dr,c+dc
                    if 0 <= rr <= self.max and 0 <= cc <= self.max and (rr,cc) not in g:
                        heapq.heappush(q, (d+1, rr,cc))
            return dist
        
        self.part1 = search()[(self.max, self.max)]

        for i in range(p1stop, len(self.data)):
            g.add(tuple(self.data[i]))
            found = search()
            if (self.max, self.max) not in found:
                self.part2 = ','.join(map(str,self.data[i]))
                break