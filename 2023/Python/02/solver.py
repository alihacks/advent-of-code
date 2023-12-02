from typing import List
import re
import math

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 8
        self.test2 = 2286

    def parse(self, instr: str) -> List:
        self.games = []
        for l in [line.split(":")[1].strip() for line in instr.splitlines()]:
            reveals = []
            for reveal in re.split(r"[:;]",l):
                r = [0,0,0]
                for cube in reveal.split(","):
                    cnt, color = cube.strip().split(" ")
                    r[["red","green","blue"].index(color)] += int(cnt)
                reveals.append(r)
            self.games.append(reveals)

    def solve(self):
        self.part1 = 0
        for id, game in enumerate(self.games):
            game_good = True
            for reveal in game:
                if reveal[0] > 12 or reveal[1] >13 or reveal[2] > 14:
                    game_good = False
                    break
            if game_good:
                self.part1 += id + 1
        
        self.part2 = 0
        for id, game in enumerate(self.games):
            maxes = [0,0,0]
            for reveal in game:
                for i in range(3):
                    maxes[i] = max([maxes[i], reveal[i]])
            self.part2 += math.prod(maxes)