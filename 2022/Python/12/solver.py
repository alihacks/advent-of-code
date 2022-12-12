from typing import List
import sys
import heapq


class Graph:
    def __init__(self, grid, start_r, start_c):
        self.grid = grid
        self.start_r, self.start_c = start_r, start_c
        self.R = len(self.grid)
        self.C = len(self.grid[0])
        self.dist = []

    def adjacents(self, r, c):
        adj = []
        if r > 0:
            adj.append((r - 1, c))
        if r < self.R - 1:
            adj.append((r + 1, c))
        if c > 0:
            adj.append((r, c - 1))
        if c < self.C - 1:
            adj.append((r, c + 1))
        return [(r1, c1) for r1, c1 in adj if self.grid[r1][c1] - self.grid[r][c] <= 1]

    def dijkstra(self):
        self.dist = [[sys.maxsize for _ in range(self.C)]
                     for _ in range(self.R)]
        self.dist[self.start_r][self.start_c] = 0
        q = [(0, self.start_r, self.start_c)]

        while q:
            d, min_r, min_c = heapq.heappop(q)
            for rr, cc in self.adjacents(min_r, min_c):
                if self.dist[rr][cc] > d + 1:
                    new_dist = d + 1
                    self.dist[rr][cc] = new_dist
                    heapq.heappush(q, (new_dist, rr, cc))

    def shortest(self, r, c):
        self.dijkstra()
        return self.dist[r][c]


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 31
        self.test2 = 29

    def parse(self, instr: str) -> List:
        self.data = [[i for i in list(line)] for line in instr.splitlines()]
        for r, row in enumerate(self.data):
            for c, val in enumerate(row):
                if val >= 'a' and val <= 'z':
                    self.data[r][c] = int(ord(val) - ord('a'))
                elif val == 'S':
                    self.data[r][c] = 0
                    self.start_r, self.start_c = r, c
                elif val == 'E':
                    self.data[r][c] = 25
                    self.end_r, self.end_c = r, c

    def solve(self):
        g = Graph(self.data, self.start_r, self.start_c)
        self.part1 = g.shortest(self.end_r, self.end_c)

        sols = []
        for r, row in enumerate(self.data):
            for c, val in enumerate(row):
                if val == 0:
                    g = Graph(self.data, r, c)
                    g.dijkstra()
                    sols.append(g.dist[self.end_r][self.end_c])
        self.part2 = min(sols)
