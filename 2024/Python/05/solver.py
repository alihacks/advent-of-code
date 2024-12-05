from typing import List
from collections import defaultdict
from functools import cmp_to_key

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 143
        self.test2 = 123

    def parse(self, instr: str) -> List:
        rules, updates = instr.split('\n\n')
        self.rules = [[int(i) for i in line.split('|')] for line in rules.splitlines()]
        self.updates = [[int(i) for i in line.split(',')] for line in updates.splitlines()]

    def solve(self):
        rd = defaultdict(list)
        for r0, r1 in self.rules:
            rd[r0].append(r1)
        
        valid_cmp = cmp_to_key(lambda a, b: 1 if a in rd[b] else -1)

        for update in self.updates:
            is_valid = True
            for r0 in rd:
                for r1 in rd[r0]:
                    if r0 in update and r1 in update:
                        if update.index(r0) > update.index(r1):
                            is_valid = False
                            break
            if is_valid:
                self.part1 += update[(len(update))//2]
            else:
                fixed = sorted(update, key=valid_cmp)
                self.part2 += fixed[(len(fixed))//2]