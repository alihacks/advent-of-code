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

    def __init__(self):
        self.children = []
        self.metadata = []


def get_node(nodes, i, md):
    node = Node()
    child_count = nodes[i]
    md_count = nodes[i + 1]
    i += 2
    for ci in range(child_count):
        i, md, child = get_node(nodes, i, md)
        node.children.append(child)
    for mi in range(md_count):
        node.metadata.append(nodes[i])
        i += 1
    return i, md + sum(node.metadata), node


def node_val(n: Node):
    if not n.children:
        return sum(n.metadata)
    val = 0
    for m in n.metadata:
        if 0 < m <= len(n.children):  # !! 1 based index
            val += node_val(n.children[m - 1])
    return val


def main(input, is_real):
    nodes = list(map(int, input[0].split(' ')))
    i = 0
    ans = 0
    while i < len(nodes):
        i, ans, root = get_node(nodes, i, 0)

    print("Part1:", ans)

    print("Part2:", node_val(root))


sample_input = r"2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
