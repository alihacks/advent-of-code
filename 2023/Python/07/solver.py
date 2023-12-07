from typing import List
from collections import Counter

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 6440
        self.test2 = 5905

    def parse(self, instr: str) -> List:
        self.data = [line.split() for line in instr.splitlines()]


    def solve(self):
        def get_type(hand): # 50 = full, 41 is four of a kind etc
            return int(("".join([str(c) for _, c in  Counter(hand).most_common()])+ "0")[0:2])
        def get_ranks(hand):
            return tuple([-"AKQJT98765432".index(c) for c in hand])
        def score(scores):
            return sum([bid * (i+1) for i, (_, _, bid) in enumerate(sorted(scores))])
        
        scores = []
        for cards, bid in self.data:
            scores.append((get_type(cards), get_ranks(cards), int(bid)))
        self.part1 = score(scores)

        def get_ranks2(hand):
            return tuple([-"AKQT98765432J".index(c) for c in hand])
        def get_type2(hand):
            nj = hand.replace("J","")
            return get_type(nj) + 10 * (len(hand) - len(nj)) #each joker adds 10
        
        scores = []
        for cards, bid in self.data:
            scores.append((get_type2(cards), get_ranks2(cards), int(bid)))
        self.part2 = score(scores)
