from typing import List
import re


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 45
        self.test2 = 112

    def parse(self, instr) -> List:
        self.x0, self.x1, self.y0, self.y1 = map(
            int, re.findall(r"-?\d+", instr.splitlines()[0])
        )

    def solve(self):
        self.part1 = 0
        self.part2 = 0

        # any xv > x1 will miss
        for xi in range(self.x1 + 1):
            # yv can't be less than y0
            # or more than -y0 since it has to come down
            for yi in range(self.y0, -self.y0 + 1):
                xv, yv = xi, yi
                x, y, max_y = [0, 0, 0]
                while True:
                    x += xv
                    y += yv
                    if y > max_y:
                        max_y = y
                    if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
                        self.part2 += 1
                        if max_y > self.part1:
                            self.part1 = max_y
                        break
                    if x > self.x1 or y < self.y0:
                        break
                    xv += 1 if xv < 0 else -1 if xv > 0 else 0
                    yv -= 1
