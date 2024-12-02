from typing import List
import operator

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 2
        self.test2 = 4

    def parse(self, instr: str) -> List:
        self.data = [[int(i) for i in line.split()] for line in instr.splitlines()]

                
    def solve(self):

        def iterate_with_removal(lst):
            for i in range(len(lst)):
                removed = lst[:i] + lst[i+1:]
                yield removed

        def is_safe(l):
            diffs = list(map(operator.sub, l[1:], l[:-1]))
            return all(x in [-1, -2, -3] for x in diffs) or all(x in [1, 2, 3] for x in diffs)
             
        self.part1 = 0
        self.part2 = 0
        for line in self.data:
            if is_safe(line):
                self.part1 += 1
                self.part2 += 1
            else:
                for removed in iterate_with_removal(line):
                    if is_safe(removed):
                        self.part2 += 1
                        break
