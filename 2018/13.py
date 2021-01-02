import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def print_grid(grid, cmax, rmax):
    for r in range(rmax):
        for c in range(cmax):
            print(grid[r][c], end='')
        print()


def turn(current, is_left):
    dirs = ['>', '^', '<', 'v']
    ti = dirs.index(current)
    ti = (ti + (1 if is_left else -1)) % 4
    return dirs[ti]


def main(input, is_real):
    part1 = None
    cmax = len(input[0])
    rmax = len(input)
    grid = [[input[r][c] for c in range(cmax)] for r in range(rmax)]
    clean_grid = copy.deepcopy(grid)

    moves = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
    left_turns = ['>/', '</', '^\\', 'v\\']
    carts = {}
    for r in range(rmax):
        for c in range(cmax):
            if grid[r][c] in ['>', '<', '^', 'v']:
                carts[(r, c)] = (grid[r][c], 0)
                clean_grid[r][c] = '-' if grid[r][c] in ['<', '>'] else '|'

    crashed = False
    tick = 0
    while True:
        tick += 1
        sorted_carts = list(carts.keys())
        sorted_carts.sort()
        for cart in sorted_carts:
            if cart not in carts:  # We may have lost this cart to a crash
                continue
            r, c = cart[0], cart[1]
            direction, ts = carts[cart]
            d_r, d_c = moves[direction]
            dst_r, dst_c = (r + d_r, c + d_c)
            dst_cell = grid[dst_r][dst_c]
            if dst_cell in ['/', '\\']:
                is_left = direction + dst_cell in left_turns
                direction = turn(direction, is_left)
            elif dst_cell == '+':
                if ts == 0:
                    direction = turn(direction, True)
                elif ts == 2:
                    direction = turn(direction, False)
                ts = (ts + 1) % 3

            grid[r][c] = clean_grid[r][c]  # We are moving, evict old cell

            # Crash detection
            if grid[dst_r][dst_c] in moves.keys():
                #print("We had a crash")
                if part1 is None:
                    part1 = f"{dst_c},{dst_r}"
                # Restore crash site
                grid[dst_r][dst_c] = clean_grid[dst_r][dst_c]
                crashed = True
                # Remove dead carts
                del carts[cart]
                del carts[(dst_r, dst_c)]
            else:  # Move it
                grid[dst_r][dst_c] = direction
                del carts[cart]
                carts[(dst_r, dst_c)] = (direction, ts)
        #print("At tick ", tick)
        #print_grid(grid, cmax, rmax)
        if crashed:
            if(len(carts) == 1):
                last_r, last_c = list(carts.keys())[0]
                part2 = f"{last_c},{last_r}"
                break

    print("Part1:", part1)

    print("Part2:", part2)


sample_input = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""

sample_lines = sample_input.strip() + "   "
sample_lines = sample_lines.splitlines()

# print("[yellow]Sample1:")
#main(sample_lines, False)


sample_input = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""

sample_lines = sample_input.strip() + "   "
sample_lines = sample_lines.splitlines()

print("[yellow]Sample2:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
