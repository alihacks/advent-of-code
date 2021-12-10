from typing import List


class Solver:
    def __init__(self, input, is_test):
        self.data = self.parse(input)
        self.is_test = is_test
        self.test1 = 26397
        self.test2 = 288957

    def parse(self, instr) -> List:
        return [list(line) for line in instr.splitlines()]

    def solve(self):
        PARENS = {")": "(", "]": "[", "}": "{", ">": "<"}
        scorelist = []
        self.part1 = 0
        for line in self.data:
            stack = []
            for sign in line:
                if sign in PARENS:
                    if stack.pop() != PARENS[sign]:
                        self.part1 += {")": 3, "]": 57, "}": 1197, ">": 25137}[sign]
                        break
                else:
                    stack.append(sign)
            else:
                # incomplete.append(line)
                score = 0
                for s in reversed(stack):
                    score = score * 5 + {"(": 1, "[": 2, "{": 3, "<": 4}[s]
                scorelist.append(score)
        scorelist.sort()
        self.part2 = scorelist[len(scorelist) // 2]
