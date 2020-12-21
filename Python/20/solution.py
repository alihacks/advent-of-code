from typing import List
import numpy as np
import copy
import math


def parse(instr: str) -> List:
    tlines = instr.split('\n\n')
    tiles = {}
    for line in tlines:
        # parts =
        name, *parts = line.strip().split('\n')
        tiles.update({name.replace('Tile ', '').replace(':', ''): parts})
    return tiles


def parse_tiles(tiles):
    result = []
    for num in tiles:
        perms = []
        keys = set()
        o_tile = copy.deepcopy(tiles[num])
        for i in range(len(o_tile)):
            o_tile[i] = list(o_tile[i])

        for tile in [o_tile, o_tile[::-1], [l[::-1] for l in o_tile], [l[::-1] for l in o_tile][::-1]]:
            for r in range(0, 4):
                rtile = copy.deepcopy(np.rot90(tile, r))
                t = {}
                t['id'] = num
                t['N'] = "".join(rtile[0])
                t['S'] = "".join(rtile[-1])
                t['E'] = "".join([t[-1] for t in rtile])
                t['W'] = "".join([t[0] for t in rtile])
                key = str(t['N']) + str(t['S']) + str(t['E']) + str(t['W'])
                if key not in keys:
                    keys.add(key)
                    t['data'] = rtile
                    perms.append(t)

        result.append([num, perms])
    return result


def tile_fits(grid, tile, x, y):
    if y > 0 and grid[x][y-1]:
        if tile['N'] != grid[x][y-1]['S']:
            return False

    if x > 0 and grid[x - 1][y]:
        if tile['W'] != grid[x - 1][y]['E']:
            return False
    return True


def find_tile(grid, tiles, x=0, y=0, used=None):
    if used is None:
        used = set()
    if (y == len(grid)):
        return grid
    x_next = x + 1
    y_next = y
    if x_next == len(grid):
        x_next = 0
        y_next += 1

    for tile in tiles:
        tile_name = tile[0]
        if tile_name in used:
            continue
        used.add(tile_name)
        for perm in tile[1]:
            if tile_fits(grid, perm, x, y):
                grid[x][y] = perm
                sol = find_tile(grid, tiles, x_next, y_next, used)
                if sol is not None:
                    return sol
        used.remove(tile_name)

    if x == 0 and y == 0:
        print(f"Exhausted w/used: {used}")
    grid[x][y] = None
    return None


def partOne(instr: str) -> int:
    tiles = parse_tiles(parse(instr))
    n = math.isqrt(len(tiles))

    grid = [[None] * n for _ in range(n)]
    puzzle = find_tile(grid, tiles)
    # print(puzzle)
    ans = int(puzzle[0][0]['id']) * int(puzzle[0][-1]['id']) * \
        int(puzzle[-1][0]['id']) * int(puzzle[-1][-1]['id'])

    return ans


def make_image(grid):
    n = len(grid)
    tilesize = 10 - 2
    cells = [[None] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            data = grid[x][y]['data']
            new_data = []
            for i in range(1, len(data) - 1):
                new_data.append(data[i][1:-1])
            cells[x][y] = new_data
    image = [[None] * n * tilesize for _ in range(n * tilesize)]
    for x in range(n * tilesize):
        for y in range(n * tilesize):
            cellx = int(x / tilesize)
            celly = int(y / tilesize)
            image[x][y] = cells[celly][cellx][x % tilesize][y % tilesize]
    return image


def find_monsters(image, monster_coords):
    n = len(image)
    monster_locs = set()
    for x in range(n):
        for y in range(n):
            is_monster = True
            mc = 0
            monster_hits = set()
            for mx, my in monster_coords:
                if x + mx < n and y + my < n:
                    if image[x + mx][y + my] != '#':
                        is_monster = False
                        break
                    else:
                        monster_hits.add((x + mx, y + my))
                else:
                    is_monster = False  # out of space to be monster
                    break
                mc += 1
            if is_monster:
                monster_locs = monster_locs.union(monster_hits)
    if len(monster_locs) > 0:
        return monster_locs


def print_image(image):
    for x in range(len(image)):
        for y in range(len(image)):
            print(image[x][y], end='')
        print()


def partTwo(instr: str) -> int:
    tiles = parse_tiles(parse(instr))
    n = math.isqrt(len(tiles))
    grid = [[None] * n for _ in range(n)]
    monstertxt = ['                  # ',
                  '#    ##    ##    ###',
                  ' #  #  #  #  #  #   ']

    monster = []
    for line in monstertxt:
        monster.append(list(line))
    monster_coords = []
    for x in range(len(monster)):
        for y in range(len(monster[0])):
            if monster[x][y] == '#':
                monster_coords.append((x, y))

    # solve puzzle
    puzzle = find_tile(grid, tiles)
    image = make_image(puzzle)

    images = []
    for m in [image, image[::-1], [l[::-1] for l in image], [l[::-1] for l in image][::-1]]:
        for r in range(0, 4):
            images.append(np.rot90(m, r))

    for image in images:
        # Count regular #s
        pixels = set()
        for x in range(len(image)):
            for y in range(len(image)):
                if (image[x][y] == "#"):
                    pixels.add((x, y))
        ans = find_monsters(image, monster_coords)
        if ans is not None:
            return len(pixels.difference(ans))

    return
