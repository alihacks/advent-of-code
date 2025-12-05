from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 3
        self.test2 = 14 

    def parse(self, instr: str) -> List:
        ranges, ingredients = instr.split('\n\n')
        self.r = [tuple(map(int,l.split('-'))) for l in ranges.splitlines()]
        self.i = [int(l) for l in ingredients.splitlines()]

    def solve(self):
        for i in self.i:
            for r in self.r:
                if i >= r[0] and i <= r[1]:
                    self.part1 += 1
                    break

        sr = sorted(self.r, key=lambda x: x[0])
        merged = []
        for s,e in sr:
            if not merged or merged[-1][1] < s:
                merged.append(tuple([s,e]))
            else: # overlap, merge it
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        for s,e in merged:
            self.part2 += e - s + 1
