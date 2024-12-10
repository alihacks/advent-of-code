from typing import List
from collections import deque

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 1928
        self.test2 = 2858

    def parse(self, instr: str) -> List:
        self.data = [int(i) for i in list(instr.split()[0])]

    def solve(self):
        def take(disk, i, n):
            res = []
            for _ in range(n):
                while disk[i][0] == 0 or disk[i][1] == -1:
                    i = i - 1
                disk[i] = (disk[i][0] - 1, disk[i][1])
                res.append(disk[i][1])
            return i, res
        
        def take2(disk, i, n):
            res = []
            while disk[i][0] == 0 or disk[i][1] == -1 or disk[i][0] > n:
                i = i - 1
                if i < 0:
                    return -1, -1
            res = [disk[i][1]] * disk[i][0];
            disk[i] = (disk[i][0],-1)
            return i, res        

        def calc(p2 = False):        
            disk = [(n,i // 2) if i % 2 == 0 else (n,-1) for i, n in enumerate(self.data)]
            res = []
            l, r = 0, len(disk) - 1
            while r >= l:
                n, val = disk[l]
                disk[l] = (0,-1)
                if val >= 0:
                    res.extend([val] * n)
                else:
                    filled = 0
                    r1 = r
                    while filled < n:
                        r1, ret = take2(disk, r1, n - filled) if p2 else take(disk, r, n)
                        if not p2:
                            r = r1
                            res.extend(ret)
                            break
                        if r1 < 0:
                            res.extend([0] * (n - filled))
                            break
                        filled += len(ret)
                        res.extend(ret)
                l+= 1
            return sum([i * n for i, n in enumerate(res)])
        
        self.part1 = calc()
        self.part2 = calc(True)

