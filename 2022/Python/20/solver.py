from typing import List
from collections import deque

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 3
        self.test2 = 1623178306

    def parse(self, instr: str) -> List:
        self.data = [int(line) for line in instr.splitlines()]

    def decrypt(self, mix_count):
        n = len(self.data)
        shuffled = list(range(n))
        vals = {i: val for i, val in enumerate(self.data)}

        for _ in range(mix_count):
            for item in list(range(n)):
                i = shuffled.index(item)
                del shuffled[i]
                shuffled.insert((i + vals[item]) % (n - 1), item)

        zi = [vals[n] for n in shuffled].index(0)
        return sum(
            vals[shuffled[(zi + i) % n]] for i in (1000, 2000, 3000))

    def solve(self):
        self.part1 = self.decrypt(1)
        for i in range(len(self.data)):
            self.data[i] *= 811589153
        self.part2 = self.decrypt(10)

