from typing import List
from itertools import permutations, product
from collections import defaultdict


class Scanner:
    def __init__(self, points):
        self.points = points
        self.perms = []

        # 6 x,y,z swaps
        for rots in permutations(range(3)):
            # each can be + or -
            for signs in product([-1, 1], repeat=3):
                new_points = []
                for point in points:
                    # TODO refac
                    new_point = [
                        signs[0] * point[rots[0]],
                        signs[1] * point[rots[1]],
                        signs[2] * point[rots[2]],
                    ]
                    # print(new_point)
                    new_points.append(new_point)
                self.perms.append(new_points)

        # print(self.perms)
        # print(len(self.perms))


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 79
        self.test2 = 3621
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr) -> List:
        self.scanners = []

        for s in instr.split("\n\n"):
            points = []
            for coord in s.strip().split("\n")[1:]:
                points.append([int(i) for i in coord.split(",")])
            self.scanners.append(Scanner(points))

    def overlaps(self, grid, offsets, perm):
        # print("ingrid", len(grid))
        for i in range(len(grid)):
            existing_scanner = grid[i]
            deltas = defaultdict(int)
            # print("check")
            for x, y, z in perm:
                for ex, ey, ez in existing_scanner:
                    dx, dy, dz = ex - x, ey - y, ez - z
                    deltas[(dx, dy, dz)] += 1
            # print(deltas)
            for (dx, dy, dz), val in deltas.items():
                if val >= 12:
                    my_x, my_y, my_z = offsets[i]
                    return [dx + my_x, dy + my_y, dz + my_z]
        return None

    def match_scanners(self, grid, offsets, seen):
        print("Matching with seen=", seen)
        if len(grid) == len(self.scanners):
            return grid
        for i in range(len(self.scanners)):
            if i in seen:
                continue
            seen.add(i)
            for perm in self.scanners[i].perms:
                # print("perm")
                deltas = self.overlaps(grid, offsets, perm)
                if deltas is not None:
                    print(i, "fits")
                    grid.append(perm)
                    offsets.append(deltas)
                    sol = self.match_scanners(grid, offsets, seen)
                    if sol is not None:
                        return sol
                    grid.pop()
                    offsets.pop()
            seen.remove(i)

        return None

    def solve(self):
        self.part1 = 0

        grid = [self.scanners[0].points]
        offsets = [[0, 0, 0]]
        seen = set([0])
        matched = self.match_scanners(grid, offsets, seen)
        # corrected = []
        beacons = set()
        for i in range(len(matched)):
            dx, dy, dz = offsets[i]
            # print(dx, dy, dz)
            for point in matched[i]:
                mx, my, mz = point
                beacons.add(tuple([mx + dx, my + dy, mz + dz]))

        self.part1 = len(beacons)

        self.part2 = 0

        for b1 in offsets:
            for b2 in offsets:
                md = abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])
                if md > self.part2:
                    self.part2 = md
