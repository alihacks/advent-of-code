from typing import List
import itertools


class Solver:
    def __init__(self, input, is_test):
        self.input = input
        self.is_test = is_test
        self.test1 = 739785
        self.test2 = 444356092776315

    def parse(self) -> List:
        return [int(line) for line in self.input.splitlines()]

    def solve1(self):
        pos = self.parse()
        scores = [0, 0]
        dice = 0
        while True:
            p = dice % 2
            pos[p] = ((pos[p] + 3 * dice + 5) % 10) + 1
            scores[p] += pos[p]
            # print("player", turn +1, "moved to", self.positions[turn], "score", s[turn])
            dice += 3
            if scores[p] >= 1000:
                break
        return dice * min(scores)

    def calc_wins(self, pos1, s1, pos2, s2):
        wins1, wins2 = 0, 0
        for dice in itertools.product([1, 2, 3], repeat=3):
            pos = (pos1 - 1 + sum(dice)) % 10 + 1
            score = s1 + pos
            if score >= 21:
                wins = (0, 1)
            elif (pos2, s2, pos, score) in self.states:
                wins = self.states[(pos2, s2, pos, score)]
            else:
                # flipped, next turn
                wins = self.calc_wins(pos2, s2, pos, score)
            wins1 += wins[1]
            wins2 += wins[0]
        self.states[(pos1, s1, pos2, s2)] = (wins1, wins2)
        return (wins1, wins2)

    def solve(self):
        self.part1 = self.solve1()
        # (p1, score1, p2, score2) -> p1_wincount, p2+wincount where p1 is next move
        self.states = {}
        pos = self.parse()
        self.part2 = max(self.calc_wins(pos[0], 0, pos[1], 0))
