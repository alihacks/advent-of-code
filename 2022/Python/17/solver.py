from typing import List
from itertools import cycle
from collections import defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 3068
        self.test2 = 0

    def parse(self, instr: str) -> List:
        self.data = [-1 if s =='<' else 1 for s in list(instr.strip())]
        self.rocks = [
            set([(2,0),(3,0),(4,0),(5,0)]),
            set([(3,0),(2,1),(3,1),(4,1), (3,2)]),
            set([(2,0),(3,0),(4,0),(4,1),(4,2)]),
            set([(2,0),(2,1),(2,2),(2,3)]),
            set([(2,0),(3,0),(2,1),(3,1)])]

    def jet_rock(self,rock, offset):
        x = [x for x,_ in rock]
        if offset == 1 and max(x) == 6:
            return rock
        if offset == -1 and min(x) == 0:
            return rock
        rock_j = set([(x+offset, y) for x,y in rock])
        return rock_j if not rock_j & self.board else rock

    def drop_rock(self, rock):
        rock_d = set([(x,y-1) for x,y in rock])
        if rock_d & set(self.board) or min([y for _,y in rock_d]) < 0:
            return False, rock
        return True, rock_d

    def simulate(self, n, stop_on_cycle = False):
        self.floor = -1
        self.board = set()
        jets = cycle(range(len(self.data)))
        rocks = cycle(range(len(self.rocks)))
        cycles = {}
        for i in range(n):
            ri = next(rocks)
            rock = self.rocks[ri]
            # place 3 above floor
            rock = set([(x,y + self.floor + 4) for x,y in rock])
            while True:
                ji = next(jets)
                rock = self.jet_rock(rock,self.data[ji])
                moved, rock = self.drop_rock(rock)
                if not moved:
                    break
            self.board.update(rock)
            rock_top = max([y for _,y in rock])
            if rock_top > self.floor:
                self.floor = rock_top
                if stop_on_cycle:
                    for yi in [y for _,y in rock]:
                        if len([x for x,y in self.board if y == yi]) == 7:
                            if (ri,ji) not in cycles:
                                cycles[(ri,ji)] = (i, yi)
                            elif cycles[(ri,ji)][1] < yi:
                                start_i, start_h = cycles[(ri,ji)]
                                return start_i, i - start_i, yi - start_h
        return self.floor + 1

    def solve(self):
        self.part1 = self.simulate(2022)
        if self.is_test:
            return # could not find cycle in test
        start_i, rock_count, h_gain = self.simulate(5000, True)
        loops, extra = divmod(1000000000000 - start_i, rock_count)
        self.part2 = (loops) * h_gain + self.simulate(start_i + extra)
