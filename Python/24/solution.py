from typing import List
import copy


def parse(instr: str) -> List:
    commands = []
    for line in instr.splitlines():
        moves = []
        i = 0
        while i < len(line):
            d = line[i]
            if d in ['w', 'e']:
                moves.append(d)
                i += 1
            else:
                moves.append(line[i: i + 2])
                i += 2
        commands.append(moves)
    return commands


def lay_tiles(cmds: list):
    xlist, ylist = [], []
    moves = {}
    moves['w'] = (-1, 0)
    moves['e'] = (1, 0)
    moves['nw'] = (-1, 1)
    moves['ne'] = (0, 1)
    moves['sw'] = (0, -1)
    moves['se'] = (1, -1)

    tilemap = {}
    for cmd in cmds:
        x, y = 0, 0
        for move in cmd:
            x_move, y_move = moves[move]
            x += x_move
            y += y_move
            xlist.append(x)
            ylist.append(y)
        if (x, y) not in tilemap:
            tilemap[(x, y)] = True
        else:  # flip
            tilemap.update({(x, y): not tilemap[(x, y)]})
    return tilemap, max([max(xlist), max(ylist)])


def partOne(instr: str) -> int:
    cmds = parse(instr)
    tilemap, _ = lay_tiles(cmds)
    ans = 0
    for _, v in tilemap.items():
        ans += 1 if v else 0
    return ans


def make_grid(tilemap, n):
    grid = [[False for _ in range(n)] for _ in range(n)]
    middle = int(n / 2)
    for k, v in tilemap.items():
        x, y = k
        if v:
            grid[middle + x][middle + y] = True
    return grid


def count_black(grid):
    cnt = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]:
                cnt += 1
    return cnt


def partTwo(instr: str) -> int:
    cmds = parse(instr)
    tilemap, n = lay_tiles(cmds)
    ni = [(-1, 0), (1, 0), (-1, 1), (0, 1), (0, -1), (1, -1)]

    iters = 100
    n = n + 2 * iters  # Max growth

    grid = make_grid(tilemap, n)
    print(count_black(grid))
    for i in range(iters):
        next_grid = copy.deepcopy(grid)
        for x in range(1, n - 1):
            for y in range(1, n - 1):
                bn = 0
                for dx, dy in ni:
                    if grid[x + dx][y + dy]:
                        bn += 1
                if (grid[x][y] and (bn == 0 or bn > 2)):
                    next_grid[x][y] = False
                if (not grid[x][y] and bn == 2):
                    next_grid[x][y] = True
        grid = next_grid
    return count_black(grid)
