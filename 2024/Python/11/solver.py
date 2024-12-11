from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 55312
        self.test2 = 65601038650482

    def parse(self, instr: str) -> List:
        self.data = list(map(int,instr.strip().split(' ')))

    def solve(self):
        self.cache = {}

        def split(stone, n):
            key = (stone,n)
            if key in self.cache:
                return self.cache[(stone,n)]
            n -= 1
            if n < 0:
                return 1
            if stone == 0:
                res = split(2024, n - 1)
            elif len(str(stone)) % 2 == 0:
                sp = len(str(stone)) // 2
                res = split(int(str(stone)[:sp]), n) + split(int(str(stone)[sp:]), n)
            else:
                res = split(stone*2024, n)
            self.cache[key] = res
            return res

        self.part1 = sum([split(i, 25) for i in self.data])
        self.part2 = sum([split(i, 75) for i in self.data])
        