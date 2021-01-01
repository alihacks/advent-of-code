import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


class Node:
    def __init__(self, val, prev, next):
        self.val = val
        self.prev = prev
        self.next = next

    def unlink(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.next

    def append(self, val):
        new = Node(val, self, self.next)
        self.next.prev = new
        self.next = new
        return new


def play(pc, lm):
    scores = collections.defaultdict(int)
    current = Node(0, None, None)
    current.prev = current
    current.next = current
    for i in range(1, lm + 1):
        cp = i % pc
        if i % 23 == 0:
            for _ in range(7):
                current = current.prev
            scores[cp] += i + current.val
            current = current.unlink()
            continue
        current = current.next.append(i)

    ans = max(scores.values())
    print((ans))
    return ans


def main(input, is_real):
    pc, lm = map(int, re.findall(r'\d+', input[0]))

    ans = play(pc, lm)
    print("Part1:", ans)
    ans = play(pc, lm * 100)
    print("Part2:", ans)


assert 32 == play(9, 25)
assert 8317 == play(10, 1618)
assert 146373 == play(13, 7999)
assert 2764 == play(17, 1104)
assert 54718 == play(21, 6111)
assert 37305 == play(30, 5807)

sample_input = r"""
9 players; last marble is worth 25 points
"""
sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
