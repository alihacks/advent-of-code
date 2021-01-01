import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def get_ranges(points):
    xmin = min([x for x, y in points])
    xmax = max([x for x, y in points])
    ymin = min([y for x, y in points])
    ymax = max([y for x, y in points])
    return xmin, ymin, xmax, ymax


def print_message(points):
    xmin, ymin, xmax, ymax = get_ranges(points)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if (x, y) in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


def is_box(points, is_real):
    _, ymin, _, ymax = get_ranges(points)
    return ymax - ymin < (10 if is_real else 9)


def main(input, is_real):
    points = []
    vels = []
    for line in input:
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        points.append((px, py))
        vels.append((vx, vy))

    secs = 0
    while True:
        secs += 1
        for i in range(len(points)):
            px, py = points[i]
            vx, vy = vels[i]
            points[i] = (px + vx, py + vy)

        if is_box(points, is_real):
            print_message(points)
            break

    print("Part1:", "See above")

    print("Part2:", secs)


sample_input = r"""
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
# exit(1)
print("[green]Real:")
main(lines, True)
