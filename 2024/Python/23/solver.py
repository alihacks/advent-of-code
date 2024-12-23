from typing import List
from collections import defaultdict, deque
import networkx

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 7
        self.test2 = 'co,de,ka,ta'

    def parse(self, instr: str) -> List:
        self.data = [line.split('-') for line in instr.splitlines()]

    def solve(self):
        g = networkx.Graph(self.data)

        for c in networkx.enumerate_all_cliques(g):
            if len(c) == 3 and any(n[0] =='t' for n in c):
                self.part1 += 1
            elif len(c) > 3: break

        self.part2 = ','.join(sorted(max(networkx.find_cliques(g), key=len)))
