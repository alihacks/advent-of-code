from typing import List
from collections import deque

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 10092
        self.test2 = 9021

    def parse(self, instr: str) -> List:
        self.grid, instr = instr.split('\n\n')
        self.instr = list(''.join(instr.splitlines()))
        self.grid2 = self.grid.replace('#','##').replace('O','[]').replace('.','..').replace('@', '@.')

    def solve(self):
        def make_grid(gridstr):
            g = [list(line) for line in gridstr.splitlines()]
            ret = {}
            for r in range(len(g)):
                for c in range(len(g[0])):
                    if g[r][c] == '@': 
                        robot = complex(r,c)
                        g[r][c] = '.'
                    ret[complex(r,c)] = g[r][c]
            return ret, robot
        
        def walk(g, robot):
            for i in self.instr:
                move = {'<':-1j, '>':1j, '^':-1, 'v':1}[i]
                n = robot + move
                if g[n] == '#':
                    continue
                elif g[n] == '.':
                    robot = n
                else:
                    moves = []
                    q = deque([robot])
                    while q:
                        pos = q.popleft()
                        if pos in moves: continue
                        moves.append(pos)
                        next_pos = pos + move
                        if g[next_pos] == '#':
                            moves = []
                            break
                        if g[next_pos] == 'O':
                            q.append(next_pos)
                        elif g[next_pos] == '[':
                            q += [next_pos, next_pos + 1j]
                        elif g[next_pos] == ']':
                            q += [next_pos, next_pos - 1j]
                    if moves:
                        for pos in moves[::-1]:
                            g[pos + move] = g[pos]
                            g[pos] = '.'
                        robot = n

            return sum([int(k.real * 100 + k.imag) for k,v in g.items() if v in ['[','O']])

        self.part1 = walk(*make_grid(self.grid))
        self.part2 = walk(*make_grid(self.grid2))