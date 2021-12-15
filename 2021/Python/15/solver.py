from typing import List
import sys
from collections import defaultdict
import heapq


class Graph:
    def __init__(self, grid, repeats=1):
        self.grid = grid
        self.repeats = repeats
        self.R = len(self.grid)
        self.C = len(self.grid[0])

    def adjacents(self, r, c):
        adj = []
        R = self.R * self.repeats
        C = self.C * self.repeats

        if r > 0:
            adj.append((r - 1, c))
        if r < R - 1:
            adj.append((r + 1, c))
        if c > 0:
            adj.append((r, c - 1))
        if c < C - 1:
            adj.append((r, c + 1))
        return adj

    def get(self, r, c):
        gv = self.grid[r % self.R][c % self.C] + (r // self.R) + (c // self.C)
        return gv % 9 if gv > 9 else gv

    def dijkstra(self):
        dist = [
            [sys.maxsize for _ in range(self.C * self.repeats)]
            for _ in range(self.R * self.repeats)
        ]
        dist[0][0] = self.grid[0][0]
        q = [(dist[0][0], 0, 0)]

        while q:
            d, min_r, min_c = heapq.heappop(q)

            for rr, cc in self.adjacents(min_r, min_c):
                if dist[rr][cc] > d + self.get(rr, cc):
                    new_dist = d + self.get(rr, cc)
                    dist[rr][cc] = new_dist
                    heapq.heappush(q, (new_dist, rr, cc))

        self.dist = dist


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 40
        self.test2 = 315

    def parse(self, instr) -> List:
        self.data = [[int(i) for i in list(line)] for line in instr.splitlines()]

    def solve(self):
        self.part1 = 0
        g = Graph(self.data)

        g.dijkstra()
        self.part1 = g.dist[g.R - 1][g.C - 1] - g.dist[0][0]

        g = Graph(self.data, 5)
        g.dijkstra()
        self.part2 = g.dist[5 * g.R - 1][5 * g.C - 1] - g.dist[0][0]
