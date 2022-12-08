from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.test1 = 21
        self.test2 = 8
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr: str) -> List:
        self.data = [list(line) for line in instr.splitlines()]

    def solve(self):
        g = self.data
        cnt = 0
        R, C = len(g), len(g[0])

        cols = [[] for _ in range(C)]
        for r in range(R):
            for c in range(C):
                cols[c].append(g[r][c])

        for r in range(R):
            for c in range(C):
                val = g[r][c]
                if r == 0 or r == R-1 or c == 0 or c == C-1:
                    cnt += 1
                    continue
                # left right
                if max(g[r][0:c]) < val or max(g[r][c+1:C]) < val:
                    cnt += 1
                    continue
                # top bot
                if max(cols[c][0:r]) < val or max(cols[c][r+1:R]) < val:
                    cnt += 1
                    continue
        self.part1 = cnt
        scores = cols = [[0 for _ in range(C)] for _ in range(R)]
        for r in range(R):
            for c in range(C):
                val = g[r][c]
                sl, sr, st, sb = 0, 0, 0, 0
                # left
                for c0 in range(c-1, -1, -1):
                    if g[r][c0] < val:
                        sl += 1
                    else:
                        sl += 1
                        break
                # right
                for c0 in range(c+1, C, 1):
                    if g[r][c0] < val:
                        sr += 1
                    else:
                        sr += 1
                        break
                # top
                for r0 in range(r-1, -1, -1):
                    if g[r0][c] < val:
                        st += 1
                    else:
                        st += 1
                        break
                # bottom
                for r0 in range(r+1, R, 1):
                    if g[r0][c] < val:
                        sb += 1
                    else:
                        sb += 1
                        break
                scores[r][c] = sl * sr * sb * st

        self.part2 = max(map(max, scores))
