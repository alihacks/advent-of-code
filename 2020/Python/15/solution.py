from typing import List


def parse(instr: str) -> List:
    for line in instr.splitlines():
        return [int(n) for n in line.split(',')]


def rindex(alist, value):
    return len(alist) - alist[-1::-1].index(value) - 1


def partOne(instr: str) -> int:
    input = parse(instr)
    lastnum = input[len(input) - 1]
    for i in range(len(input), 2020):
        if lastnum in input[:-1]:
            lastspoken = i - 1
            prevspoken = rindex(input[:lastspoken], lastnum)
            newnum = lastspoken - prevspoken
            input.append(newnum)
            lastnum = newnum
        else:
            input.append(0)
            lastnum = 0

    return input[-1]


# optimize, don't keep whole list
def partTwo(instr: str) -> int:
    input = parse(instr)
    lastnum = input[len(input) - 1]
    cache = {}
    for i in range(0, len(input)):
        cache.update({input[i]: [-1, i]})

    for i in range(len(input), 30000000):
        if lastnum not in cache or cache[lastnum][0] == -1:
            lastnum = 0
            cache[lastnum] = (cache[lastnum][1], i)
        else:
            lastnum = cache[lastnum][1] - cache[lastnum][0]
            if lastnum not in cache:
                cache[lastnum] = (-1, i)
            else:
                cache[lastnum] = (cache[lastnum][1], i)

    return lastnum
