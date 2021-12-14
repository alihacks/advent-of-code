from typing import List
from collections import Counter


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 1588
        self.test2 = 2188189693529

    def parse(self, instr) -> List:
        self.lookup = {}
        for line in instr.splitlines():
            if line and "->" in line:
                parts = line.split(" -> ")
                self.lookup[parts[0]] = parts[1]
            elif line:
                self.input = line

    def solve(self):
        c = Counter([self.input[i : i + 2] for i in range(len(self.input) - 1)])
        for i in range(40):
            new_c = Counter()
            for pair in c:
                # NC will result in Nb and bC
                p0, p1 = pair[0], pair[1]
                middle = self.lookup[p0 + p1]
                new_c[p0 + middle] += c[pair]
                new_c[middle + p1] += c[pair]
            c = new_c

            if i + 1 in [10, 40]:
                letters = Counter()
                for pair in c:
                    letters[pair[0]] += c[pair]
                # pairs overlap, we look at first chars, so add last char
                # if we had ABC our pairs are Ab Bc so we count, A and B already, add C
                letters[self.input[-1]] += 1
                commons = letters.most_common()
                ans = commons[0][1] - commons[-1][1]
                if i + 1 == 10:
                    self.part1 = ans
                else:
                    self.part2 = ans
