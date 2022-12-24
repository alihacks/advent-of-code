from typing import List
from collections import deque, defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 18
        self.test2 = 54

    def parse(self, instr: str) -> List:
        self.data = defaultdict(set)
        lines = instr.splitlines()
        self.R = len(lines) - 2
        self.C = len(lines[0]) - 2
        for r, line in enumerate(lines):
            for c,v in enumerate(line):
                if v not in ['.','#']:
                    self.data[v].add((r - 1,c - 1))


    def solve(self):
        deltas = {'v':(1,0), '^': (-1,0), '<': (0,-1), '>':(0,1)}

        def travel(start, end, t_start):
            def next_at_time(t,r,c): # possible moves from r,c at time t
                n = []
                for dr, dc in [(1,0), (-1,0), (0,-1), (0,1), (0,0)]:
                    r1, c1 = r + dr, c + dc
                    if (r1,c1) in [start, end]: # special cases start and end
                        n.append((r1,c1))
                        continue
                    if r1 < 0 or c1 < 0 or r1 >= self.R or c1 >= self.C:
                            continue
                    collision = False
                    for k in deltas:
                        #if (r1,c1) in [((d[0] + deltas[k][0] * t) %self.R, (d[1] + deltas[k][1] * t) % self.C) for d in self.data[k]]:
                        # above was too slow, move math to the left
                        if ((r1 - deltas[k][0] * t) % self.R, (c1 - deltas[k][1] * t) % self.C) in self.data[k]:
                            collision = True
                            break
                    if not collision:
                        n.append((r1,c1))
                return n

            q = deque([(start[0], start[1], t_start)])
            seen = set()   
            while q:
                re, ce, t = q.popleft()
                t += 1
                next_moves = next_at_time(t,re, ce)
                if end in next_moves:
                    return t
                for r1, c1 in next_moves:
                    if(r1,c1,t) not in seen:
                        seen.add((r1,c1,t))
                        q.append((r1,c1, t))

        home, goal = (-1,0), (self.R, self.C - 1 )
        self.part1 = travel(home, goal, 0)
        self.part2 = travel(home, goal, travel(goal, home, self.part1))
