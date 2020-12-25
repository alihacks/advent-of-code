from typing import List
import copy


MOVES = {'w': (-1, 0), 'e': (1, 0), 'nw': (-1, 1),
         'ne': (0, 1), 'sw': (0, -1), 'se': (1, -1)}


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

    black_tiles = set()
    for cmd in cmds:
        x, y = 0, 0
        for move in cmd:
            x_move, y_move = MOVES[move]
            x += x_move
            y += y_move
        if (x, y) not in black_tiles:
            black_tiles.add((x, y))
        else:  # flip back to white
            black_tiles.remove((x, y))
    return black_tiles


def partOne(instr: str) -> int:
    cmds = parse(instr)
    black_tiles = lay_tiles(cmds)
    return len(black_tiles)


def partTwo(instr: str) -> int:
    cmds = parse(instr)
    tilemap = lay_tiles(cmds)
    ni = [v for _, v in MOVES.items()]

    iters = 100

    for i in range(iters):
        next_map = set()
        to_visit = set()
        for (x, y) in tilemap:
            to_visit.add((x, y))
            for dx, dy in ni:
                to_visit.add((x + dx, y + dy))

        for (x, y) in to_visit:
            bn = 0
            for dx, dy in ni:
                if (x + dx, y + dy) in tilemap:
                    bn += 1
            if (x, y) in tilemap and not (bn == 0 or bn > 2):
                next_map.add((x, y))
            if (not (x, y) in tilemap and bn == 2):
                next_map.add((x, y))
        tilemap = next_map
    return len(tilemap)
