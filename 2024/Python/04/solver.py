from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 18
        self.test2 = 9

    def parse(self, instr: str) -> List:
        self.data = [list(line) for line in instr.splitlines()]

    def solve(self):
        G = self.data
        R = len(G)
        C = len(G[0])
        
        def search(r, c, dr, dc, str):
            for i in range(len(str)):
                new_r = r + i * dr
                new_c = c + i * dc
                if new_r not in range(R) or new_c not in range(C):
                    return False
                if G[new_r][new_c] != str[i]:
                    return False
            return True
        
        def search_bidirectional(r, c, dr, dc, str):
            return search(r, c, dr, dc, str) or search(r, c, dr, dc, str[::-1])
                
        for r in range(R):
            for c in range(C):
                for dr, dc in [(0, 1), (1, 0),(1, 1), (-1, 1)]:
                    if search_bidirectional(r, c, dr, dc, 'XMAS'):
                        self.part1 += 1
                if r in range(1, R - 1) and c in range(1, C - 1):
                    if G[r][c] == 'A' and search_bidirectional(r-1, c-1, 1, 1, 'MAS') and search_bidirectional(r+1, c-1, -1, 1, 'MAS'):
                        self.part2 += 1