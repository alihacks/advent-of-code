from typing import List
import math


class Grid:
    def __init__(self, input_string):
        self.grid = []
        for line in input_string.splitlines():
            self.grid.append(list(map(int, list(line))))
        self.R = len(self.grid)
        self.C = len(self.grid[0])

    def is_valid_coord(self, r, c):
        return r >= 0 and r < self.R and c >= 0 and c < self.C

    def neighbor_coords(self, r, c):
        n = []
        if self.is_valid_coord(r - 1, c):
            n.append([r - 1, c])
        if self.is_valid_coord(r, c - 1):
            n.append([r, c - 1])
        if self.is_valid_coord(r + 1, c):
            n.append([r + 1, c])
        if self.is_valid_coord(r, c + 1):
            n.append([r, c + 1])
        return n

    def find_lowpoints(self):
        res = []
        for r in range(self.R):
            for c in range(self.C):
                neighbors = []
                for nr, nc in self.neighbor_coords(r, c):
                    neighbors.append(self.grid[nr][nc])

                if self.grid[r][c] < min(neighbors):
                    res.append([r, c])
        return res

    def make_basin(self, current, new):
        to_visit = set()
        current = current.union(new)
        for r, c in new:
            for nr, nc in self.neighbor_coords(r, c):
                if (nr, nc) not in current:  # not visited yet
                    if self.grid[nr][nc] < 9:  # did not hit a 9
                        to_visit.add((nr, nc))
        if len(to_visit):
            current = self.make_basin(current, to_visit)
        return current


def partOne(instr: str) -> int:
    g = Grid(instr)
    ans = 0
    for r, c in g.find_lowpoints():
        ans += g.grid[r][c] + 1

    return ans


def partTwo(instr: str) -> int:
    g = Grid(instr)
    basins = []
    for r, c in g.find_lowpoints():
        basin = g.make_basin(set(), set([(r, c)]))
        basins.append(len(basin))
    basins.sort(reverse=True)
    ans = math.prod(basins[0:3])

    return ans
