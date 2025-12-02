from typing import List


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 1227775554 
        self.test2 = 4174379265

    def parse(self, instr: str) -> List:
        #print(instr.split(','))
        self.data = [line.split('-') for line in instr.strip().split(',')]


    def solve(self):

        def invalid(input, p2 = False):
            n = str(input)
            for i in range(2, len(n) + 1 if p2 else  3):
                chunk = n[:len(n) // i]
                if chunk * i == n:
                    return True

        for pair in self.data:
            for n in range(int(pair[0]), int(pair[1]) + 1):
                if invalid(n):
                    self.part1 += n
                if invalid(n, True):
                    self.part2 += n
 
