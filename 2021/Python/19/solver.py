from typing import List
from itertools import permutations, product
from collections import defaultdict


class Scanner:
    def __init__(self, points):
        self.points = points
        self.perms = []
        # pre-compute all permutations, start with x,y,z switching
        for rots in permutations(range(3)):
            # add sign change: + or -
            for signs in product([-1, 1], repeat=3):
                new_points = []
                for point in points:
                    new_point = [signs[i] * point[rots[i]] for i in range(3)]
                    new_points.append(new_point)
                self.perms.append(new_points)


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 79
        self.test2 = 3621

    def parse(self, instr) -> List:
        self.scanners = []

        for s in instr.split("\n\n"):
            points = []
            for coord in s.strip().split("\n")[1:]:
                points.append([int(i) for i in coord.split(",")])
            self.scanners.append(Scanner(points))

    def overlaps(self, perm):
        for existing_scanner, (m_x, m_y, m_z) in self.matched:
            deltas = defaultdict(int)
            for x, y, z in perm:
                for ex, ey, ez in existing_scanner:
                    dx, dy, dz = ex - x, ey - y, ez - z
                    deltas[(dx, dy, dz)] += 1

            for (dx, dy, dz), val in deltas.items():
                if val >= 12:
                    return [dx + m_x, dy + m_y, dz + m_z]
        return None

    def match_scanners(self):
        print("Matching with seen=", self.seen)
        if len(self.matched) == len(self.scanners):
            return self.matched
        for i in range(len(self.scanners)):
            if i in self.seen:
                continue
            self.seen.add(i)
            for perm in self.scanners[i].perms:
                # print("perm")
                deltas = self.overlaps(perm)
                if deltas is not None:
                    print(i, "fits")
                    self.matched.append([perm, deltas])
                    sol = self.match_scanners()
                    if sol is not None:
                        return sol
                    self.matched.pop()
            self.seen.remove(i)

        return None

    def solve(self):
        # first scanner is 0,0,0 as-is
        self.matched = [[self.scanners[0].points, [0, 0, 0]]]
        self.seen = set([0])
        self.match_scanners()
        beacons = set()
        for points, (dx, dy, dz) in self.matched:
            for mx, my, mz in points:
                beacons.add(tuple([mx + dx, my + dy, mz + dz]))

        self.part1 = len(beacons)
        self.part2 = 0

        for _, (x1, y1, z1) in self.matched:
            for _, (x2, y2, z2) in self.matched:
                md = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
                if md > self.part2:
                    self.part2 = md
