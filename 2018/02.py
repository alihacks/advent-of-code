from collections import Counter
from itertools import combinations
from rich import print
from aocd import lines, get as aocd_get


def main(input, is_real):
    counts = [Counter(s) for s in input]
    twos = sum(1 for c in counts if 2 in c.values())
    threes = sum(1 for c in counts if 3 in c.values())
    ans = twos * threes
    print("Part1:", ans)

    for s1, s2 in combinations(input, 2):
        commons = "".join([c1 for c1, c2 in zip(s1, s2) if c1 == c2])
        if len(commons) == len(s1) - 1:
            print("Part2:", commons)
            break


sample_input = r"""
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
