from typing import List
from collections import defaultdict


class Solver:
    def __init__(self, input, is_test):
        self.data = self.parse(input)
        self.is_test = is_test
        self.test1 = 226
        self.test2 = 3509

    def parse(self, instr) -> List:
        self.graph = defaultdict(list)
        for n1, n2 in [line.split("-") for line in instr.splitlines()]:
            self.graph[n1].append(n2)
            self.graph[n2].append(n1)

    def find_paths(self, path: List):
        # print("Here with", path)
        for neighbor in self.graph[path[-1]]:
            if neighbor.islower() and neighbor in path:
                continue
            path.append(neighbor)
            if neighbor == "end":
                self.part1 += 1
            else:
                self.find_paths(path)
            path.pop()

    def find_paths2(self, path: List, sc):
        for neighbor in self.graph[path[-1]]:
            if neighbor == "start":
                continue
            if neighbor.islower() and neighbor in path:
                if sc != neighbor:  # special neighbor has been picked already
                    continue
                elif (
                    path.count(neighbor) > 1
                ):  # this is our special char so it can occur once
                    continue

            path.append(neighbor)
            if neighbor == "end":
                ps = ",".join(path)
                if ps not in self.seen2:
                    self.seen2.add(ps)
                    self.part2 += 1
                    # print("sc", sc, "Terminal:", path)
            else:
                self.find_paths2(path, sc)
            path.pop()

    def solve(self):
        self.part1 = 0
        self.part2 = 0

        self.find_paths(["start"])

        self.seen2 = set()
        # would have be been easier with BFS but part1 was already DFS so brute force it
        for node in [k for k in self.graph.keys() if k.islower()]:
            self.find_paths2(["start"], node)
