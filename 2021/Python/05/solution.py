from typing import List
from collections import Counter


class Line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    # Get points between 2 numbers regardles of direction
    @staticmethod
    def points_between(start, end):
        if end > start:
            return range(start, end + 1)
        return list(range(start, end - 1, -1))

    def get_straight_points(self) -> List:
        points = []
        if self.x0 == self.x1:
            for y in self.points_between(self.y0, self.y1):
                points.append(tuple([self.x0, y]))
        elif self.y0 == self.y1:
            for x in self.points_between(self.x0, self.x1):
                points.append(tuple([x, self.y0]))
        return points

    def get_all_points(self) -> List:
        points = self.get_straight_points()
        if points:
            return points
        if abs(self.x1 - self.x0) == abs(self.y1 - self.y0):
            line_len = abs(self.x1 - self.x0)
            for delta in range(line_len + 1):
                dx = delta if self.x1 > self.x0 else -delta
                dy = delta if self.y1 > self.y0 else -delta
                points.append(tuple([self.x0 + dx, self.y0 + dy]))
        return points


def parse(instr: str) -> List:
    lines = []
    for start, stop in [line.split(" -> ") for line in instr.splitlines()]:
        x0, y0 = [int(i) for i in start.split(",")]
        x1, y1 = [int(i) for i in stop.split(",")]
        lines.append(Line(x0, y0, x1, y1))
    return lines


def partOne(instr: str) -> int:
    lines = parse(instr)
    c = Counter()
    for line in lines:
        c.update(line.get_straight_points())

    return len([count for _, count in c.items() if count > 1])


def partTwo(instr: str) -> int:
    lines = parse(instr)
    c = Counter()
    for line in lines:
        c.update(line.get_all_points())

    return len([count for _, count in c.items() if count > 1])
