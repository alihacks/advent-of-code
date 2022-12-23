from typing import List
from collections import deque
from copy import deepcopy

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 110
        self.test2 = 20

    def parse(self, instr: str) -> List:
        self.data = set()
        for r, line in enumerate(instr.splitlines()):
            for c,v in enumerate(line):
                if v == '#':
                    self.data.add((r,c))

    def play(self, p2 = False):
        moves = deque([((-1,-1),(-1,0),(-1,1)), # N
            ((1,-1), (1,0), (1,1)), # S
            ((-1,-1),(0,-1),(1,-1)), # W
            ((-1,1),(0,1),(1,1)) ]) # E
        grid = deepcopy(self.data)
        def ta(t1, t2):
            return ((t1[0] + t2[0]), (t1[1] + t2[1]))

        def lonely(elf):
            for delta in [(-1,-1),(-1,0),(-1,1),(1,-1), (1,0), (1,1),(0,-1),(0,1)]:
                if ta(elf,delta) in grid:
                    return False
            return True

        for i in range(100000 if p2 else 10):
            d1 = []
            seen, dups = set(), set()
            moved = False
            for r,c in grid:
                elf = (r,c)
                if not lonely(elf):
                    for m in moves:
                        if ta(elf,m[0]) not in grid and ta(elf,m[1]) not in grid and ta(elf,m[2]) not in grid:
                            elf = ta(elf,m[1])
                            moved = True
                            break
                if elf in seen:
                    dups.add(elf)
                seen.add(elf)
                d1.append((elf[0], elf[1],r,c))
            grid = set()
            for r1,c1, r0, c0 in d1:
                r, c = (r0,c0) if (r1,c1) in dups else (r1, c1)
                grid.add((r,c))
                if p2 and not moved:
                    return i + 1
            moves.rotate(-1)
        rs = [r for r,_ in grid]
        cs = [c for _,c in grid]
        return (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1) - len(grid)

    def solve(self):
        self.part1 = self.play()
        self.part2 = self.play(True)
