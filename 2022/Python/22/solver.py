from typing import List
import re

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 6032
        self.test2 = 0

    def parse(self, instr: str) -> List:
        grid, steps = instr.split('\n\n')
        grid = grid.splitlines()
        self.steps = re.findall(r'\d+|[RL]', steps)
        self.C = max([len(line) for line in grid])
        self.grid = [f'{line:{self.C}}' for line in grid]
        self.R = len(self.grid)

    def play(self, p2 = False):
        r, c= 0, self.grid[0].index('.')
        dirs, dir = [(0,1), (1,0), (0,-1), (-1,0)], 0

        def next_spot(r,c,d):
            cd = dirs[d]
            r1 = r + cd[0]
            c1 = c + cd[1]
            if not p2:
                return r1 % self.R, c1 % self.C, d
            else:
                # See cube.png for numbers!!
                if r1 == -1: #fell off top 
                    if c1 >= 100 : # from 2
                        r1, c1 = 199, c1 - 100
                    else: # from 1
                        d = 0
                        r1, c1 = c1 + 100, 0                        
                elif c1 == -1 and cd[1] == -1: # fell off left
                    if r1 >= 150: # from 6
                        d = 1
                        r1, c1 = 0, r1 - 100
                    else: # from 4
                        d = 0
                        r1, c1 = 149 - r1, 50
                
                elif r1 == self.R: # fell off bottom == from 6
                    r1, c1 = 0, c1 + 100
                elif c1 == 150 and cd[1] == 1: # fell off right == from 2
                    d = 2
                    r1, c1 = 149 - r1, 99

                # fell off middle to left (1,3)
                elif c1 == 49:
                    if r1 < 50: # 1
                        d = 0
                        r1, c1 = 149 - r1, 0
                    elif r1 < 100: # 3
                        d = 1
                        r1, c1 = 100, r1 - 50

                # fell off middle to right (3,5)
                elif c1 == 100:
                    if r1 >= 100: # 5
                        d = 2
                        r1, c1 = 149 - r1, 149
                    elif r1 >= 50: # 3
                        d = 3
                        r1, c1 = 49, r1 + 50

                # fell off middle to bottom from #5
                elif r1 == 150 and c1 >=50 and cd[0] == 1:
                    d = 2
                    r1, c1 = c1 + 100, 49

                # fell right from 6 to 5
                elif r1 >= 150 and c1 == 50:
                    d = 3
                    r1, c1 = 149, r1 - 100

                # fell up from 4
                elif r1 == 99 and c1 < 50:
                    d = 0
                    r1, c1 = c1 + 50, 50
                
                # fell down from 2
                elif r1 == 50 and c1 >= 100:
                    d = 2
                    r1, c1 = c1 - 50, 99
                return r1, c1, d

        def move(r,c,d):
            while True:
                r,c,d = next_spot(r,c,d)
                if self.grid[r][c] != " ":
                    return r,c,d

        for step in self.steps:
            if step == 'R':
                dir = (dir + 1) % 4
            elif step == 'L':
                dir = dir - 1 if dir > 0 else 3
            else:
                for _ in range(int(step)):
                    r1, c1, d1 = move(r,c,dir)
                    if self.grid[r1][c1] == "#":
                        break
                    r, c, dir = r1, c1, d1
        return 1000 * (r + 1) + 4 * (c + 1) + dir

    def solve(self):
        self.part1 = self.play()
        if self.is_test: # test is not helpful / diff shape
            return
        self.part2 = self.play(True)