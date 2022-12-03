from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 157
        self.test2 = 70
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [list(line) for line in instr.splitlines()]

    def pri(self, letter):
        o = ord(letter)
        if o >= ord('a'):
            return o - ord('a') + 1
        return o - ord('A') + 27

    def solve(self):
        for bag in self.data:
            mid = len(bag) // 2
            match = set(bag[:mid]).intersection(set(bag[mid:]))
            letter = list(match)[0]
            self.part1 += self.pri(letter)

        sets = list(map(set, self.data))
        for i in range(0, len(self.data), 3):
            match = set.intersection(*sets[i:i+3])
            self.part2 += self.pri(list(match)[0])
