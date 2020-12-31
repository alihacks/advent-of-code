import collections
import functools
import operator
import itertools
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def closest(coords, x, y):
    dst = [None for _ in range(len(coords))]
    for i in range(len(coords)):
        cx, cy = coords[i]
        dst[i] = abs(x - cx) + abs(y - cy)
    return dst.index(min(dst)), sum(dst)


def main(input, is_real):
    ans = 0
    p2 = 0
    coords = []
    buffer = 10000 if is_real else 32
    max_coord = 0
    for line in input:
        [x, y] = map(int, line.split(','))
        coords.append((x, y))
        max_coord = max(max_coord, x, y)
    n = max_coord + 1

    grid = [[None for _ in range(n)] for _ in range(n)]
    infinites = set()
    for x, y in itertools.product(range(n), range(n)):
        ix, td = closest(coords, x, y)
        grid[x][y] = ix
        if td < buffer:
            p2 += 1
        if x in [0, n - 1] or y in [0, n - 1]:
            infinites.add(ix)

    counts = collections.Counter(itertools.chain.from_iterable(grid))
    for ci in set(range(len(coords))) - infinites:
        ans = max(ans, counts[ci])

    print("Part1:", ans)

    print("Part2:", p2)


sample_input = r"""
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
