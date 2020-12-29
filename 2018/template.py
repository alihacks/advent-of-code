from collections import *
from itertools import *
import re
from rich import print
from aocd import lines, get as aocd_get


def main(input, is_real):
    ans = input[0]

    print("Part1:", ans)

    print("Part2:", ans)


sample_input = r"""
sample
lines
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
