from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 13140
        self.test2 = 0
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [line.split(' ') for line in instr.splitlines()]

    def solve(self):
        reg = 1
        cy = 1
        vals = {}
        for cmd in self.data:
            vals[cy] = reg
            if cmd[0] == 'noop':
                cy += 1
                continue
            else:
                vals[cy+1] = reg
                reg += int(cmd[1])
                cy += 2

        for cycle in [20, 60, 100, 140, 180, 220]:
            self.part1 += cycle * vals[cycle]

        self.part2 = '\n'
        for line in range(6):
            for i in range(1, 41):
                if vals[line*40+i] in [i-2, i-1, i]:
                    self.part2 += '#'
                else:
                    self.part2 += '.'
            self.part2 += '\n'
