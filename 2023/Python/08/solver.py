from typing import List
import re, math, itertools

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 2
        self.test2 = 2

    def parse(self, instr: str) -> List:
        self.steps, nodes = instr.strip().split("\n\n")
        self.nodes = {}
        for line in nodes.split("\n"):
            key, vals = line.split(" = ")
            l,r = re.findall(r"[A-Z0-9]+", vals)
            self.nodes[key] = {"L": l, "R": r}

    def solve(self):
        def count_steps(curr, end):
            for c in itertools.count():
                curr = self.nodes[curr][self.steps[c % len(self.steps)]]
                if curr.endswith(end):
                    return c + 1

        self.part1 = count_steps("AAA", "ZZZ")
        self.part2 = math.lcm(*[count_steps(n, "Z") for n in self.nodes if n[-1] == "A"])
