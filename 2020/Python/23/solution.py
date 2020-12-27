from typing import List


def parse(instr: str) -> List:
    return list([int(i) for i in instr.splitlines()[0]])


def play_cups(input, next, iters):
    max_cup = len(input)
    for i in range(max_cup):
        next_loc = 0 if i + 1 >= max_cup else i + 1
        next[input[i]] = input[next_loc]
    current_cup = input[0]

    for i in range(iters):
        p1 = next[current_cup]
        p2 = next[p1]
        p3 = next[p2]
        dst = current_cup - 1 if current_cup > 1 else max_cup
        while dst in [p1, p2, p3]:
            dst -= 1
            if dst == 0:
                dst = max_cup
        next[current_cup] = next[p3]
        next[p3] = next[dst]
        next[dst] = p1
        current_cup = next[current_cup]


def partOne(instr: str) -> int:
    iters = 100
    input = parse(instr)
    next = [None for _ in range(len(input) + 1)]

    play_cups(input, next, iters)
    ans = ''
    cc = 1
    while next[cc] != 1:
        cc = next[cc]
        ans += str(cc)
    return ans


def partTwo(instr: str) -> int:
    iters = 10000000
    input = parse(instr)

    # Add cups
    for m in range(max(input) + 1, 1000000 + 1):
        input.append(m)
    next = [None for _ in range(len(input) + 1)]

    play_cups(input, next, iters)

    return next[1] * next[next[1]]
