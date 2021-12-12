from typing import List
from collections import defaultdict, deque


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

    def bfs(self, double_small):
        q = deque([("start", set(["start"]), None)])
        ans = 0
        while q:
            n, smalls, special_small = q.popleft()
            if n == "end":
                ans += 1
                continue
            for neighbor in self.graph[n]:
                if neighbor not in smalls:
                    new_smalls = set(smalls)
                    if neighbor.islower():
                        new_smalls.add(neighbor)
                    q.append((neighbor, new_smalls, special_small))

                elif (
                    double_small
                    and special_small is None
                    and neighbor not in ["start", "end"]
                ):
                    q.append((neighbor, smalls, neighbor))
        return ans

    def solve(self):
        self.part1 = self.bfs(False)
        self.part2 = self.bfs(True)
