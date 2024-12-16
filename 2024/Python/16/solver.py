from typing import List
import heapq

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 11048
        self.test2 = 64

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
        def search(p2=False):
            q = [(0,*self.end,dir)for dir in range(4)] if p2 else [(0,*self.start,1)]
            dist = {}
            while q:
                d,r,c,dir = heapq.heappop(q)
                if (r,c,dir) in dist: continue
                dist[(r,c,dir)] = d
                dr,dc = moves[(dir + 2) % 4] if p2 else moves[dir]
                rr,cc = r+dr,c+dc
                if (rr,cc) in self.g:
                    heapq.heappush(q, (d+1, rr,cc,dir))
                for nd in {0:[1,3], 1:[2,0], 2:[3,1], 3:[0,2]}[dir]:
                    heapq.heappush(q, (d + 1000, r,c,nd))    
            return dist
        
        dist = search()
        self.part1 = min([dist[(r,c,d)] for r,c,d in dist if (r,c) == self.end])
        dist2 = search(True)
        best_seats = set()
        for r,c,_ in [k for k in dist if k in dist2 and dist[k] + dist2[k] == self.part1]:
            best_seats.add((r,c))
        self.part2 = len(best_seats)