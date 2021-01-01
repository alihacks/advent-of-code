import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def get_power(x, y, serial):
    power = y * (x + 10) + serial
    power *= x + 10
    return int(str(power)[-3]) - 5


def get_max(grid, boxsize):
    maxp = 0
    maxloc = None
    search_range = 300 - boxsize - 1
    for x0 in range(search_range):
        for y0 in range(search_range):
            x, y = x0 + 1, y0 + 1
            totp = 0
            for dx in range(boxsize):
                for dy in range(boxsize):
                    totp += grid[x0+dx][y0+dy]
            if totp > maxp:
                maxp = totp
                maxloc = x, y
    return maxloc, maxp


def main(input, is_real):
    serial = int(input[0])
    grid = [[0 for y in range(300)] for x in range(300)]

    for x0, y0 in itertools.product(range(300), range(300)):
        x, y = x0 + 1, y0 + 1
        grid[x0][y0] = get_power(x, y, serial)

    ans, _ = get_max(grid, 3)
    print("Part1:", ans)

    maxloc = None
    maxbox = 0
    maxpow = 0
    for s in range(2, 15):
        # print(s)
        l, p = get_max(grid, s)
        if p > maxpow:
            maxpow = p
            maxloc = l
            maxbox = s
    print(f"Part2: {maxloc[0]},{maxloc[1]},{maxbox}")


sample_input = r"""
42
"""

sample_lines = sample_input.strip().splitlines()

assert 4 == get_power(3, 5, 8)
assert -5 == get_power(122, 79, 57)
assert 0 == get_power(217, 196, 39)
assert 4 == get_power(101, 153, 71)

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
