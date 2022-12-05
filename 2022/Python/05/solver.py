from typing import List
import re
import copy


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = "CMZ"
        self.test2 = "MCD"
        self.part1 = ""
        self.part2 = ""

    def parse(self, instr: str) -> List:
        self.stacks = [[] for _ in range(11)]
        self.instr = []
        p1, p2 = instr.split("\n\n")
        p1 = p1.splitlines()
        for r in range(len(p1) - 1):
            line = list(p1[r])
            for c, val in enumerate(line):
                if val.isalpha():
                    self.stacks[(c-1) // 4 + 1].append(val)
        for line in p2.splitlines():
            self.instr.append(list(map(int, re.findall(r"[0-9]+", line))))

    def get_tops(self, stacks):
        val = ""
        for stack in stacks:
            if len(stack) > 0:
                val += stack[0]
        return val

    def solve(self):
        stacks = copy.deepcopy(self.stacks)
        for cnt, src, dst in self.instr:
            for i in range(cnt):
                val = stacks[src].pop(0)
                stacks[dst].insert(0, val)
        self.part1 = self.get_tops(stacks)

        stacks = self.stacks.copy()
        for cnt, src, dst in self.instr:
            val = ""
            for i in range(cnt):
                val = stacks[src].pop(0) + val
            for char in val:
                stacks[dst].insert(0, char)
        self.part2 = self.get_tops(stacks)
