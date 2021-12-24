from typing import List


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 0
        self.test2 = 0
        self.part1 = 0
        self.part2 = 0

    def parse(self, instr):
        self.chunks = [i.split("\n")[:-1] for i in instr.split("inp w\n")[1:]]

    # input to python compiler
    # only used for experimentation, make a func for each digit
    def compile(self):
        CMDS = {"add": "+", "mul": "*", "div": "//", "mod": "%"}
        funcs = []
        for i, chunk in enumerate(self.chunks):
            code = "def fun" + str(i) + "(w,x,y,z):\n"
            for cmd, op1, op2 in [i.split(" ") for i in chunk]:
                code += "  "
                if cmd in CMDS:
                    code += op1 + "=" + op1 + CMDS[cmd] + op2
                elif cmd == "eql":
                    code += op1 + "= 1 if " + op1 + " == " + op2 + " else 0"
                code += "\n"
            code += "  return z\n"

            code += "funcs.append(fun" + str(i) + ")"
            exec(code)
        return funcs

    def find_different_literals(self):
        diff_i = []
        for i in range(len(self.chunks[0])):
            all_same = all(
                self.chunks[y][i] == self.chunks[0][i] for y in range(len(self.chunks))
            )
            if not all_same:
                diff_i.append(i)
        # get different literals
        lits = []
        for chunk in self.chunks:
            lits.append([int(chunk[i].split(" ")[-1]) for i in diff_i])
        return map(list, zip(*lits))

    def solve(self):
        if self.is_test:  # no testing :(
            return
        DIGITS = 14
        # we have 3 literals
        # a is either 26 or 1
        a, b, c = self.find_different_literals()
        # a is always 26 if b < 0, so a is useless
        for i in range(DIGITS):
            assert (a[i] == 26) == (b[i] < 0)

        deltas, digits = [], []
        for i in range(DIGITS):
            if b[i] > 0:
                digits.append((i, c[i]))
            else:
                j, ci = digits.pop()
                deltas.append([i, j, ci + b[i]])

        # start with max/min possible
        self.part1 = [9 for _ in range(DIGITS)]
        self.part2 = [1 for _ in range(DIGITS)]

        # apply deltas to pass checks
        for i, j, delta in deltas:
            assert i > j  # j is most sig digit
            if delta > 0:
                self.part1[j] -= delta
                self.part2[i] += delta
            else:
                self.part1[i] += delta
                self.part2[j] -= delta
            # delta must match
            assert self.part1[i] - self.part1[j] == delta
            assert self.part2[i] - self.part2[j] == delta

        self.part1 = "".join([str(i) for i in self.part1])
        self.part2 = "".join([str(i) for i in self.part2])
