from typing import List
from collections import defaultdict


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 17
        self.test2 = "\n#####\n#   #\n#   #\n#   #\n#####\n"

    def parse(self, instr) -> List:
        self.dots = set()
        self.folds = []
        for line in instr.splitlines():
            if line.startswith("fold"):
                instr = line.replace("fold along ", "").split("=")
                self.folds.append([instr[0] == "y", int(instr[1])])
            elif "," in line:
                self.dots.add(tuple([int(i) for i in line.split(",")]))

    def fold(self, fold_line, is_y):
        new_dots = set()
        for x, y in self.dots:
            if is_y and y > fold_line:
                new_dots.add((x, 2 * fold_line - y))
            elif not is_y and x > fold_line:
                new_dots.add((2 * fold_line - x, y))
            else:
                new_dots.add((x, y))
        self.dots = new_dots

    def dots_to_str(self):
        res = "\n"
        X = max([x for x, _ in self.dots])
        Y = max([y for _, y in self.dots])
        for y in range(Y + 1):
            for x in range(X + 1):
                if (x, y) in self.dots:
                    res += "#"
                else:
                    res += " "
            res += "\n"
        return res

    def solve(self):
        self.part1 = None
        self.part2 = 0
        for is_y, fold_line in self.folds:
            self.fold(fold_line, is_y)
            if self.part1 == None:
                self.part1 = len(self.dots)

        self.part2 = self.dots_to_str()
