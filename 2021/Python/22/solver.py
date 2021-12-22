from typing import List
import re


class Cube:
    def __init__(self, x0, x1, y0, y1, z0, z1, is_on):
        self.x0, self.x1 = x0, x1
        self.y0, self.y1 = y0, y1
        self.z0, self.z1 = z0, z1
        self.is_on = is_on
        if is_on:
            self.size = (x1 + 1 - x0) * (y1 + 1 - y0) * (z1 + 1 - z0)
        else:
            self.size = 0

    def intersection(self, c2):
        x0 = max(self.x0, c2.x0)
        x1 = min(self.x1, c2.x1)
        y0 = max(self.y0, c2.y0)
        y1 = min(self.y1, c2.y1)
        z0 = max(self.z0, c2.z0)
        z1 = min(self.z1, c2.z1)
        if x0 <= x1 and y0 <= y1 and z0 <= z1:
            return Cube(x0, x1, y0, y1, z0, z1, self.is_on)

    # return resulting cubes from intersection
    def subtract(self, c2):
        res = []
        ci = self.intersection(c2)
        if not ci:
            return []

        x0, x1 = self.x0, self.x1
        y0, y1 = self.y0, self.y1
        z0, z1, is_on = self.z0, self.z1, self.is_on

        if ci.x0 > x0:  # left cuboid
            res.append(Cube(x0, ci.x0 - 1, y0, y1, z0, z1, is_on))
        if x1 > ci.x1:  # right cuboid
            res.append(Cube(ci.x1 + 1, x1, y0, y1, z0, z1, is_on))

        if ci.y0 > y0:  # bottom cuboid
            res.append(Cube(ci.x0, ci.x1, y0, ci.y0 - 1, z0, z1, is_on))
        if y1 > ci.y1:  # top cuboid
            res.append(Cube(ci.x0, ci.x1, ci.y1 + 1, y1, z0, z1, is_on))

        if ci.z0 > z0:  # front cuboid
            res.append(Cube(ci.x0, ci.x1, ci.y0, ci.y1, z0, ci.z0 - 1, is_on))
        if z1 > ci.z1:  # back cuboid
            res.append(Cube(ci.x0, ci.x1, ci.y0, ci.y1, ci.z1 + 1, z1, is_on))
        return res


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 590784
        self.test2 = 2758514936282235

    def parse(self, instr) -> List:
        self.cmds = []
        for line in instr.splitlines():
            d = [line[0:2] == "on"] + [int(i) for i in re.findall(r"-?\d+", line)]
            self.cmds.append(d)

    # def solve1(self):
    #     on = set()
    #     for is_on, (x0, x1), (y0, y1), (z0, z1) in self.cmds:
    #         if x0 < -50 or x0 > 50 or y0 < -50 or y0 > 50 or z0 < -50 or z0 > 50:
    #             break
    #         for xi in range(x0, x1 + 1):
    #             for yi in range(y0, y1 + 1):
    #                 for zi in range(z0, z1 + 1):
    #                     if is_on:
    #                         on.add((xi, yi, zi))
    #                     else:
    #                         on.discard((xi, yi, zi))
    #     return len(on)

    def doit(self, stop50):
        ans = 0
        seen = set()
        for is_on, x0, x1, y0, y1, z0, z1 in self.cmds:
            if stop50:
                if x0 < -50 or x0 > 50 or y0 < -50 or y0 > 50 or z0 < -50 or z0 > 50:
                    break

            c = Cube(x0, x1, y0, y1, z0, z1, is_on)
            for c2 in list(seen):
                if c.intersection(c2) is not None:
                    # replace cube we change with the new cube
                    seen.remove(c2)
                    seen.update(c2.subtract(c))
            seen.add(c)
        for c in seen:
            ans += c.size
        return ans

    def solve(self):
        self.part1 = self.doit(True)
        self.part2 = self.doit(False)
