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
    def __init__(self, val, next):
        self.val = val
        self.next = next


def print_nodes(start, last):
    n = start
    while True:
        print(n.val, end=" ")
        if n == last:
            break
        n = n.next

    print()


def check_seq(seq_start, seq):
    s = seq_start
    strval = ""
    for c in seq:
        if str(s.val) != c:
            return False
        s = s.next
    return True

    return strval == seq


def do_loops(n, seq=None):
    e1 = Node(3, None)
    e2 = Node(7, e1)
    e1.next = e2
    last = e2
    a_start = e2
    seq_start = e1
    recipes = 2
    while recipes < n + 10 or seq is not None:
        s = e1.val + e2.val
        n1 = Node(s // 10, None)
        n2 = Node(s % 10, None)
        n1.next = n2
        n2.next = last.next
        last.next = n1 if n1.val > 0 else n2
        nodes_added = 2 if n1.val > 0 else 1
        last = n2
        for _ in range(e1.val + 1):
            e1 = e1.next
        for _ in range(e2.val + 1):
            e2 = e2.next
        while nodes_added > 0:  # increment answer place
            nodes_added -= 1
            if recipes <= n:
                a_start = a_start.next
            recipes += 1
            if seq is not None and recipes > len(seq):  # part2
                seq_start = seq_start.next
                if check_seq(seq_start, seq):
                    return recipes - len(seq)

    # part 1
    ans = ""
    n = a_start
    for i in range(10):
        ans += str(n.val)
        n = n.next
    # print(ans)
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
