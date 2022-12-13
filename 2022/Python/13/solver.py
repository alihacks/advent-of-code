from typing import List
from functools import cmp_to_key


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 13
        self.test2 = 140

    def parse(self, instr: str) -> List:
        self.data = [eval(p) for p in instr.splitlines() if p]

    def compare(self, l, r):
        if isinstance(l, int):
            if isinstance(r, int):
                return 0 if l == r else 1 if l > r else -1
            return self.compare([l], r)
        if isinstance(r, int):
            return self.compare(l, [r])
        if isinstance(l, list) and isinstance(r, list):
            for left, right in zip(l, r):
                res = self.compare(left, right)
                if res != 0:
                    return res
            # see if we exhausted one list
            return self.compare(len(l), len(r))

    def solve(self):
        for i in range(0, len(self.data), 2):
            if self.compare(self.data[i], self.data[i+1]) == -1:
                self.part1 += i // 2 + 1

        self.data += [[[2]], [[6]]]
        self.data.sort(key=cmp_to_key(self.compare))
        self.part2 = 1 + self.data.index([[2]])
        self.part2 *= 1 + self.data.index([[6]])
