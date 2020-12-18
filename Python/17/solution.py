from typing import List
import copy


def parse(instr: str) -> List:
    return [
        line
        for line in instr.splitlines()
    ]


def partOne(instr: str) -> int:
    reps = 6
    growth = reps * 2  # grow in both dirs
    input = parse(instr)
    Z = 1 + growth
    R = len(input) + growth
    C = len(input[0]) + growth
    grid = [[['.' for _ in range(C)]
             for _ in range(R)] for _ in range(Z)]
    # grid[Z][C][R]
    # copy input
    for r in range(len(input)):
        for c in range(len(input[r])):
            grid[reps][c + reps][r + reps] = input[r][c]

    for iter in range(reps):
        next_grid = copy.deepcopy(grid)
        for z in range(Z):
            for c in range(C):
                for r in range(R):
                    active_neighbors = 0
                    for dz in (z - 1, z, z + 1):
                        for dc in (c - 1, c, c + 1):
                            for dr in (r - 1, r, r + 1):
                                if not (z == dz and c == dc and r == dr) \
                                        and (0 <= dz < Z) \
                                        and (0 <= dc < C) \
                                        and (0 <= dr < R) \
                                        and grid[dz][dc][dr] == '#':
                                    active_neighbors += 1
                    if grid[z][c][r] == '#' and active_neighbors != 2 and active_neighbors != 3:
                        next_grid[z][c][r] = '.'
                    elif grid[z][c][r] == '.' and active_neighbors == 3:
                        next_grid[z][c][r] = '#'
        grid = next_grid

    cnt = 0
    for z in range(Z):
        for c in range(C):
            for r in range(R):
                if grid[z][c][r] == '#':
                    cnt += 1

    return cnt


def partTwo(instr: str) -> int:
    reps = 6
    growth = reps * 2  # grow in both dirs
    input = parse(instr)
    Z = 1 + growth
    W = Z
    R = len(input) + growth
    C = len(input[0]) + growth
    grid = [[[['.' for _ in range(C)]
              for _ in range(R)] for _ in range(Z)]for _ in range(W)]
    # grid[W][Z][C][R]
    # copy input
    for r in range(len(input)):
        for c in range(len(input[r])):
            grid[reps][reps][c + reps][r + reps] = input[r][c]

    for iter in range(reps):
        next_grid = copy.deepcopy(grid)
        for w in range(W):
            for z in range(Z):
                for c in range(C):
                    for r in range(R):
                        active_neighbors = 0
                        for dw in (w - 1, w, w + 1):
                            for dz in (z - 1, z, z + 1):
                                for dc in (c - 1, c, c + 1):
                                    for dr in (r - 1, r, r + 1):
                                        if not (w == dw and z == dz and c == dc and r == dr) \
                                                and (0 <= dw < W) \
                                                and (0 <= dz < Z) \
                                                and (0 <= dc < C) \
                                                and (0 <= dr < R) \
                                                and grid[dw][dz][dc][dr] == '#':
                                            active_neighbors += 1
                        if grid[w][z][c][r] == '#' and active_neighbors != 2 and active_neighbors != 3:
                            next_grid[w][z][c][r] = '.'
                        elif grid[w][z][c][r] == '.' and active_neighbors == 3:
                            next_grid[w][z][c][r] = '#'
        grid = next_grid

    cnt = 0
    for w in range(W):
        for z in range(Z):
            for c in range(C):
                for r in range(R):
                    if grid[w][z][c][r] == '#':
                        cnt += 1

    return cnt
