from typing import List
from collections import defaultdict

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 13
        self.test2 = 30

    def parse(self, instr: str) -> List:
        self.data = [list(map(str.split, line.split(": ")[1].split("|"))) for line in instr.splitlines()]

    def solve(self):
        self.part1 = 0
        cards = defaultdict(int)
        for n, (winners, nums) in enumerate(self.data):
            cnt = len(set(winners) & set(nums))
            if cnt:
                self.part1 += 2 ** (cnt - 1)
            cards[n] += 1
            for i in range(cnt):
                cards[i + 1 + n] += cards[n]
        self.part2 = sum(cards.values())
