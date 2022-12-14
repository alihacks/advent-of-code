from typing import List
import re
from copy import deepcopy
from itertools import pairwise


def lrange(s, e):
    return range(min(s, e), max(s, e) + 1)


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 24
        self.test2 = 93

    def parse(self, instr: str) -> List:
        self.data = set()
        for line in instr.splitlines():
            points = [list(map(int, coord.split(',')))
                      for coord in re.findall(r'\d+,\d+', line)]
            for (x0, y0), (x1, y1) in pairwise(points):
                for x in lrange(x0, x1):
                    for y in lrange(y0, y1):
                        self.data.add((x, y))

    def is_free(self, x, y, floor=None):
        return (x, y) not in self.data and y != floor

    def play(self, use_floor=False):
        max_y = max(y for _, y in self.data)
        floor = None
        if use_floor:
            floor = max_y + 2
            max_y = floor
        i = 0
        while True:
            x, y = 500, 0
            while True:
                if y == max_y:  # fell
                    return i
                elif self.is_free(x, y + 1, floor):  # down
                    y += 1
                elif self.is_free(x - 1, y + 1, floor):  # left
                    x, y = x-1, y+1
                elif self.is_free(x + 1, y + 1, floor):  # right
                    x, y = x+1, y+1
                elif y == 0:  # stuck on top
                    return i + 1
                else:
                    self.data.add((x, y))
                    break
            i += 1

    def solve(self):
        data = deepcopy(self.data)
        self.part1 = self.play()
        self.data = data
        self.part2 = self.play(True)
