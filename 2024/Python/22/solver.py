from typing import List
from collections import defaultdict
from itertools import pairwise
from more_itertools import windowed

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 37990510
        self.test2 = 23

    def parse(self, instr: str) -> List:
        self.data = [int(line) for line in instr.splitlines()]

    def solve(self):
        def gen(n, cnt):
            res = [n % 10]
            for _ in range(cnt):
                n ^= (n << 6) % 2**24
                n ^= (n >> 5) % 2**24
                n ^= (n << 11) % 2**24
                res.append(n % 10)
            return n, res
        
        bids = defaultdict(int)
        for num in self.data:
            n, r = gen(num,2000)
            self.part1 += n
            seen = set()
            for i, delta in enumerate(windowed([j - i for i, j in pairwise(r)],4)):
                if delta not in seen:
                    seen.add(delta)
                    bids[delta] += r[i+4]
        self.part2 = max(bids.values())
