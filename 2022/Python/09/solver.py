from typing import List
from itertools import pairwise


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 88
        self.test2 = 36
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [line.split(" ") for line in instr.splitlines()]

    def solve(self):
        N = 10
        rope = [(0, 0)] * N
        p1, p2 = set(), set()
        deltas = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        for direction, n in self.data:
            for _ in range(int(n)):
                dr, dc = deltas[direction]
                rope[0] = (rope[0][0] + dr, rope[0][1] + dc)
                for H, T in pairwise(range(N)):
                    diff = (rope[H][0] - rope[T][0], rope[H][1] - rope[T][1])
                    if abs(diff[0]) >= 2 or abs(diff[1]) >= 2:
                        rope[T] = (rope[T][0] + 1 if diff[0] > 0 else -1 if diff[0] < 0 else 0,
                                   rope[T][1] + 1 if diff[1] > 0 else -1 if diff[1] < 0 else 0)
                p1.add(rope[1])
                p2.add(rope[T])

        self.part1 = len(p1)
        self.part2 = len(p2)
