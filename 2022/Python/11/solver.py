from typing import List
from copy import deepcopy
import re
from math import prod


class Monkey:
    def __init__(self):
        self.items = []


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 10605
        self.test2 = 2713310158
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = []
        parts = [line.splitlines() for line in instr.split('\n\n')]
        for lines in parts:
            m = Monkey()
            m.num = int(lines[0][-2])
            m.items = list(map(int, re.findall(r'\d+', lines[1])))
            m.op = lines[2].split('=')[1].strip().replace('old', 'item')
            m.mod = int(lines[3].split(' ')[-1])
            m.true_throw = int(lines[4][-1])
            m.false_throw = int(lines[5][-1])
            self.data.append(m)

    def monkey_business(self, rounds, divisor):
        monkeys = deepcopy(self.data)
        inspects = [0 for _ in range(len(monkeys))]
        p = prod([m.mod for m in monkeys])
        for r in range(rounds):
            for m in monkeys:
                for item in m.items:
                    level = eval(m.op)
                    if divisor > 1:
                        level //= divisor
                    else:
                        level %= p
                    inspects[m.num] += 1
                    dest = m.true_throw if level % m.mod == 0 else m.false_throw
                    monkeys[dest].items.append(level)
                m.items = []  # threw all

        inspects.sort()
        return inspects[-1] * inspects[-2]

    def solve(self):
        self.part1 = self.monkey_business(20, 3)
        self.part2 = self.monkey_business(10000, 0)
