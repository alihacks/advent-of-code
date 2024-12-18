from typing import List
import re
from itertools import batched


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = '4,6,3,5,6,3,5,2,1,0'
        self.test2 = 0

    def parse(self, instr: str) -> List:
        data = list(map(int,re.findall(r'\d+', instr)))
        self.a, self.b, self.c, *self.instr = data
        self.il = len(self.instr)

    def solve(self):
        def run(a):
            b, c = self.b, self.c
            ip = 0
            def combo(val):
                return {0:0, 1:1, 2:2, 3:3, 4:a, 5:b, 6:c}[val]
            buf = []
            while ip < self.il:
                op, val = self.instr[ip:ip+2]
                if op == 0:
                    a = a >> combo(val)
                elif op == 1:
                    b = b ^ val
                elif op == 2:
                    b = combo(val) % 8
                elif op == 3:
                    if a != 0:
                        ip = val
                        continue
                elif op == 4:
                    b = b ^ c
                elif op == 5:
                    buf.append(combo(val) % 8)
                elif op == 6:
                    b = a >> combo(val)
                elif op == 7:
                    c = a >> combo(val)
                ip += 2
            return buf
        
        self.part1 = ','.join(map(str,run(self.a)))

        if self.is_test: return
        solutions = [0]
        il = len(self.instr)
        for i in range(il):
            potentials = []
            for a in range(8): #one octal digit predicts an instruction
                for n in solutions:
                    guess = n << 3 | a
                    if self.instr[il-1-i:] == run(guess): # does it produce our digit?
                        potentials.append(guess)
            solutions = potentials
        self.part2 = min(solutions)
