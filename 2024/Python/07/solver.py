from typing import List
import itertools, more_itertools

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 3749
        self.test2 = 11387

    def parse(self, instr: str) -> List:
        self.data = [list(map(int,line.replace(':','').split(' '))) for line in instr.splitlines()]

    def solve(self):
        def compute(p2 = False):
            tot = 0
            operators = ['+', '*', '|'] if p2 else ['+','*']
            for eq in self.data:
                for ops in itertools.product(operators, repeat=len(eq) - 1):
                    res, op = 0, '+'
                    for el, op in zip(eq[1:], ops):
                        if op == '+':
                            res = res + el
                        elif op == '*':
                            res = res * el
                        elif op == '|':
                            res = int(str(res) + str(el))
                    if res == eq[0]:
                        tot += res
                        break
            return tot

        self.part1 = compute()
        self.part2 = compute(True)