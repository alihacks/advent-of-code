from typing import List
from collections import deque, defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 36
        self.test2 = 81

    def parse(self, instr: str) -> List:
        data = [list(line) for line in instr.splitlines()]
        self.g = defaultdict(int)
        for r in range(len(data)):
            for c in range(len(data[0])):
                self.g[complex(r,c)] = int(data[r][c])

    def solve(self):
        r = set()
        q = deque([(i,i) for i in self.g.keys() if self.g[i] == 0])
        while q:
            src,i = q.popleft()
            if self.g[i] == 9:
                self.part2 += 1
                r.add((src,i))
                continue            
            for d in [1, -1, 1j, -1j]:
                if  self.g[i+d] == self.g[i] + 1:
                    q.append((src,i+d))
        self.part1 = len(r)
        
