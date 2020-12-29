from collections import *
from itertools import *
import re
from rich import print
from aocd import lines, get as aocd_get


def main(input, is_real):
    world = {}
    for line in input:
        _, x, y, xc, yc = map(int, re.findall(r'\d+', line))
        for xi in range(x, x + xc):
            for yi in range(y, y + yc):
                world[(xi, yi)] = 1 if (
                    xi, yi) not in world else world[(xi, yi)] + 1

    print("Part1:", sum(1 for _, v in world.items() if v >= 2))

    for line in input:
        claimno, x, y, xc, yc = map(int, re.findall(r'\d+', line))
        nolap = True
        for xi in range(x, x + xc):
            for yi in range(y, y + yc):
                if world[(xi, yi)] > 1:
                    nolap = False
        if nolap:
            print("Part2:", claimno)


sample_input = r"""
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
