from typing import List


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 1656
        self.test2 = 195

    def parse(self, input_string) -> List:
        self.grid = []
        for line in input_string.splitlines():
            self.grid.append(list(map(int, list(line))))
        self.R = len(self.grid)
        self.C = len(self.grid[0])

    def print_grid(self):
        for r in range(self.R):
            print("".join([str(i) for i in self.grid[r]]))

    def get_neighbor_coords(self, r, c):
        coords = []
        for rr in range(r - 1, r + 2):
            for cc in range(c - 1, c + 2):
                if (rr, cc) != (r, c) and 0 <= rr < self.R and 0 <= cc < self.C:
                    coords.append((rr, cc))
        return coords

    def solve(self):
        step = 0
        self.part1 = 0
        self.part2 = 0

        while True:
            step += 1
            fc = 0
            flashed = []
            for r in range(self.R):
                for c in range(self.C):
                    self.grid[r][c] += 1
                    if self.grid[r][c] > 9:
                        self.grid[r][c] = 0
                        flashed.append((r, c))
            while flashed:
                r, c = flashed.pop(0)
                fc += 1
                # increase neighbors
                for rr, cc in self.get_neighbor_coords(r, c):
                    if self.grid[rr][cc] == 0:
                        continue
                    self.grid[rr][cc] += 1
                    if self.grid[rr][cc] > 9:
                        self.grid[rr][cc] = 0
                        flashed.append((rr, cc))
            if step <= 100:
                self.part1 += fc
            if fc == self.R * self.C:
                self.part2 = step
                break
