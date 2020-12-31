import collections
import functools
import operator
from itertools import *
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def reduce_polymer(instr):
    newstr = instr
    while True:
        for c in map(chr, range(ord('a'), ord('z') + 1)):
            s1 = c + c.upper()
            newstr = newstr.replace(s1, "").replace(s1[::-1], "")
        if len(instr) == len(newstr):
            return instr
        instr = newstr


def main(input, is_real):
    instr = input[0]

    print("Part1:", len(reduce_polymer(instr)))

    ans = len(instr)
    for c in map(chr, range(ord('a'), ord('z') + 1)):
        newstr = instr.replace(c, '').replace(c.upper(), '')
        ans = min(ans, len(reduce_polymer(newstr)))

    print("Part2:", ans)


sample_input = r"""
dabAcCaCBAcCcaDA
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
