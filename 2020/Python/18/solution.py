from typing import List


def parse(instr: str) -> List:
    return [
        line
        for line in instr.splitlines()
    ]


def solve(p: str, is_advanced=False) -> int:
    sol = 0
    op = '+'
    found = True
    #print(f"Solving: {p}")
    # solve parens
    while found:
        found = False
        i = 0
        while i < len(p):
            if p[i] == '(':
                found = True
                i += 1
                start = i
                while p[i] != ')':
                    if p[i] == '(':
                        start = i + 1
                    i += 1
                #print(f"Found sub {start} to {i}: {p[start:i]}")
                subst = solve(p[start:i], is_advanced)
                p = p[0:start - 1] + str(subst) + p[i + 1:]
                # print(p)
                break
            i += 1
    #print(f"Reduced to: {p}")

    # Do all the adding first in advanced mode
    if is_advanced:
        l = p.split(" ")
        for i in range(0, len(l)):
            if l[i] == "+":
                l[i + 1] = str(int(l[i - 1]) + int(l[i + 1]))
                l[i - 1] = ""
                l[i] = ""
        p = " ".join(l)

    # Regular math
    op = '+'
    i = 0
    while i < len(p):
        is_num = False
        snum = ''
        while i < len(p) and '0' <= p[i] <= '9':
            is_num = True
            snum += p[i]
            i += 1

        if is_num:
            num = int(snum)
            # print(f"num={num}")
            if op == '+':
                sol += num
            else:
                sol *= num
        elif p[i] in ('+', '*'):
            op = p[i]
        i += 1
    return sol


def partOne(instr: str) -> int:
    problems = parse(instr)
    ans = 0
    for line in problems:
        sol = solve(line)
        ans += sol
    return ans


def partTwo(instr: str) -> int:
    problems = parse(instr)
    ans = 0
    for line in problems:
        sol = solve(line, True)
        ans += sol
    return ans
