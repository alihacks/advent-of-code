import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def do_loops(n, seq=None):
    r = [3, 7]
    i1, i2 = 0, 1
    seq = list(map(int, seq)) if seq else None
    seq_len = len(seq) if seq else None
    recipes = 2
    while recipes < n + 10 or seq is not None:
        n1, n2 = divmod(r[i1] + r[i2], 10)
        added = 1
        if n1 > 0:
            r.append(n1)
            added += 1
        r.append(n2)
        recipes += added
        i1 = (i1 + r[i1] + 1) % recipes
        i2 = (i2 + r[i2] + 1) % recipes
        if seq is not None:  # part 2
            for i in range(added):
                if r[-1 * seq_len - i:][:seq_len] == seq:
                    return recipes - seq_len - i

    # part 1
    ans = "".join(map(str, r[n - recipes:]))[:10]
    return ans


def main(input, is_real):
    loops = int(input[0])
    ans = do_loops(loops)

    print("Part1:", ans)
    ans = do_loops(-1, str(loops))
    print("Part2:", ans)


assert '5158916779' == do_loops(9)
assert '0124515891' == do_loops(5)
assert '9251071085' == do_loops(18)
assert '5941429882' == do_loops(2018)

assert 9 == do_loops(-1, '51589')
assert 5 == do_loops(-1, '01245')
assert 18 == do_loops(-1, '92510')
assert 2018 == do_loops(-1, '59414')

main("9", False)
print("[green]Real:")
main(lines, True)
