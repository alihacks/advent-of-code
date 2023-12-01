from typing import List
import re


class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 142
        self.test2 = 281

    def parse(self, instr: str) -> List:
        self.data = [line for line in instr.splitlines()]

    def chop(self,l, n):
        l, rest = l[0:n], l[n:]
        l = l.replace("one","1").replace("two","2").replace("three","3") \
            .replace("four","4").replace("five","5").replace("six","6") \
            .replace("seven","7").replace("eight","8").replace("nine","9")
        return l + rest


    def solve(self):
        for l in self.data:
            digits = re.findall("[1-9]", l)
            if len(digits):
                self.part1 += int(digits[0] + digits[-1])

            line2 = l
            for n in range(2,len(line2)):
                line2 = self.chop(line2,n)            
            digits = re.findall("[1-9]",line2)

            self.part2 += int(digits[0] + digits[-1])
