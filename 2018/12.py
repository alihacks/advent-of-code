import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def count_plants(state, offset):
    cnt = 0
    for i in range(len(state)):
        if state[i] == '#':
            cnt += i - offset
    return cnt


def main(input, is_real):
    state = list(input[0].split(':')[1].strip())
    rules = {}
    for r in input[2:]:
        parts = r.split(" => ")
        if parts[1] == '#':
            rules[parts[0]] = parts[1]

    pad = ['.' for _ in range(4)]
    loops = 100000  # it won't reach this
    repeat_threshold = 20  # it will stop if it finds a repeat of 20
    buf = collections.deque(maxlen=repeat_threshold)
    pc = 0
    for i in range(loops):
        if i == 20:
            ans = count_plants(state, len(pad) * i)
            print("Part1:", ans)

        tc = count_plants(state, len(pad) * i)
        buf.append(tc - pc)
        if i > 20 and len(buf) == repeat_threshold and len(set(buf)) == 1:  # nothing new
            growth_rate = buf[0]
            break
        pc = tc

        state = pad + state + pad
        next_state = copy.deepcopy(state)
        for p in range(2, len(state) - 2):
            lookup = "".join(state[p-2:p+3])
            if lookup in rules:
                next_state[p] = rules[lookup]
            else:
                next_state[p] = '.'
        state = next_state

    ans = count_plants(state, len(pad) * i) + growth_rate * (50000000000 - i)
    print("Part2:", ans)


sample_input = r"""
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
# 3561 too lo
