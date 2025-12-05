from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 13
        self.test2 = 43 

    def parse(self, instr: str) -> List:
        s = instr.strip().splitlines()
        self.data = set()
        for r in range(len(s)):
            line = s[r]
            for c in range(len(line)):
                if line[c] == '@':
                    self.data.add((r,c))

    def solve(self):
        first = True
        removed = 1
        while removed > 0:
            next = set()
            removed = 0
            for loc in self.data:
                c = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if (loc[0]+dr,loc[1]+dc) in self.data:
                            c += 1
                if c <= 4:
                    removed += 1
                else:
                    next.add(loc)
            if first:
                first = False
                self.part1 = removed
            self.part2 += removed
            self.data = next
