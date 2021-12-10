from typing import List


def parse(instr: str) -> List:
    return [list(line) for line in instr.splitlines()]


PARENS = {")": "(", "]": "[", "}": "{", ">": "<"}


def find_incomplete(input_list):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    incomplete = []
    part1 = 0
    for line in input_list:
        stack = []
        for sign in line:
            if sign in PARENS:
                if stack.pop() != PARENS[sign]:
                    part1 += scores[sign]
                    break
            else:
                stack.append(sign)
        else:
            incomplete.append(line)
    return incomplete, part1


def partOne(instr: str) -> int:
    _, ans = find_incomplete(parse(instr))
    return ans


def partTwo(instr: str) -> int:
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    scorelist = []
    incomplete, _ = find_incomplete(parse(instr))
    for line in incomplete:
        d = []
        for sign in line:
            if sign in PARENS:
                d.pop()
            else:
                d.append(sign)
        score = 0
        for s in reversed(d):
            score = score * 5 + scores[s]
        scorelist.append(score)

    scorelist.sort()
    return scorelist[len(scorelist) // 2]
