from typing import List
import ast


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 4140
        self.test2 = 3993
        self.part1 = 0
        self.part2 = 0

    def make_tokens(self, s):
        tokens = []
        i = 0
        while i < len(s):
            if s[i] in ["[", "]", ","]:
                tokens.append(s[i])
                i += 1
            elif s[i].isdigit():
                num = ""
                while i < len(s) and s[i].isdigit():
                    num += s[i]
                    i += 1
                tokens.append(int(num))
            else:
                i += 1
        return tokens

    def parse(self, instr) -> List:
        self.lines = [self.make_tokens(line) for line in instr.splitlines()]

    # make string to print for debug
    def strt(self, t):
        return "".join([str(i) for i in t])

    def add(self, a, b):
        res = ["["] + a + [","] + b + ["]"]
        # print("after add", self.strt(res))
        reducing = True
        while reducing:
            reducing = False
            explode_res = self.apply_explode(res)
            if explode_res is not None:
                res = explode_res
                # print("exploded\t", self.strt(res))
                reducing = True
                continue
            split_res = self.apply_split(res)
            if split_res is not None:
                res = split_res
                # print("split\t", self.strt(res))
                reducing = True
        # return self.apply_reduce(res)
        return res

    def apply_split(self, tokens):
        for i in range(len(tokens)):
            ti = tokens[i]
            if isinstance(ti, int) and ti > 9:
                return (
                    tokens[:i]
                    + ["[", ti // 2, ",", (ti + 1) // 2, "]"]
                    + tokens[i + 1 :]
                )
        return None

    def apply_explode(self, tokens):
        depth = 0
        i = 0
        lastnum_i = None
        while i < len(tokens):
            if tokens[i] == "[":
                depth += 1
                if depth > 4:
                    n1, n2 = tokens[i + 1], tokens[i + 3]
                    # print("TOO DEEP", n1, n2)
                    if lastnum_i is not None:
                        # print("add", n1, "to", tokens[lastnum_i])
                        tokens[lastnum_i] += n1
                    for j in range(i + 4, len(tokens)):
                        if isinstance(tokens[j], int):
                            # print("add", n2, "to", tokens[j])
                            tokens[j] += n2
                            break
                    tokens = tokens[0:i] + [0] + tokens[i + 5 :]
                    # print("new", "".join([str(i) for i in tokens]))
                    return tokens
            elif tokens[i] == "]":
                depth -= 1
            elif isinstance(tokens[i], int):
                lastnum_i = i
            i += 1
        return None

    def magnitude(self, i):
        if isinstance(i, list):
            return 3 * self.magnitude(i[0]) + 2 * self.magnitude(i[1])
        else:
            return i

    def solve(self):
        res = None
        lines = self.lines
        for line in lines:
            if res is None:
                res = line
            else:
                res = self.add(res, line)

        res = self.strt(res)
        self.part1 = self.magnitude(ast.literal_eval(res))

        self.part2 = 0
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i != j:
                    s = self.strt(self.add(lines[i], lines[j]))
                    n = self.magnitude(ast.literal_eval(s))
                    if n > self.part2:
                        self.part2 = n
