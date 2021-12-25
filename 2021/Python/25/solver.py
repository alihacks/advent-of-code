from typing import List
import copy


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 58
        self.test2 = 0
        self.part2 = 0

    def parse(self, instr) -> List:
        self.data = [list(line) for line in instr.splitlines()]

    def print_grid(grid):
        for row in grid:
            print("".join(row))
        print("-" * 10)

    def solve(self):
        self.part1 = 0
        R = len(self.data)
        C = len(self.data[0])
        grid = self.data

        # Solver.print_grid(grid)
        step = 0
        while True:
            next_grid = copy.deepcopy(grid)
            moves = 0
            step += 1
            for r in range(R):
                for c in range(C):
                    if grid[r][c] == ">":
                        if grid[r][(c + 1) % C] == ".":
                            next_grid[r][c] = "."
                            next_grid[r][(c + 1) % C] = ">"
                            moves += 1
            grid = copy.deepcopy(next_grid)
            for r in range(R):
                for c in range(C):
                    if grid[r][c] == "v":
                        if grid[(r + 1) % R][c] == ".":
                            # print("v down")
                            next_grid[r][c] = "."
                            next_grid[(r + 1) % R][c] = "v"
                            moves += 1
            grid = next_grid
            if moves == 0:
                self.part1 = step
                break

            # print("after", i + 1, "steps")
            # Solver.print_grid(grid)
