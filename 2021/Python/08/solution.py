from collections import defaultdict
from typing import List


def parse(instr: str):
    left, right = [], []
    for line in instr.splitlines():
        parts = line.split(" | ")
        left.append(parts[0].split(" "))
        right.append(parts[1].split(" "))
    return left, right


def partOne(instr: str) -> int:
    l, r = parse(instr)
    ans = 0
    for row in r:
        for val in row:
            if len(val) in [2, 4, 3, 7]:
                ans += 1
    return ans


# return first item of length
def get_by_length(l: list, length: int):
    return list(filter(lambda i: len(i) == length, l))


# returns only one item in set b that's not in set a
def get_diff(a, b):
    diff = set(a) - set(b)
    assert (len(diff)) == 1
    return list(diff)[0]


# returns only one item that intersects
def get_common(a, b):
    i = set(a).intersection(set(b))
    assert (len(i)) == 1
    return list(i)[0]


# return only one item from list that contains all elements
def filter_contains(l, elements):
    res = list(filter(lambda i: set(elements).issubset(set(i)), l))
    assert len(res) == 1
    return res[0]


def decode(row: List):
    segments = {}
    digits = {}
    digits[1] = get_by_length(row, 2)[0]
    digits[4] = get_by_length(row, 4)[0]
    digits[7] = get_by_length(row, 3)[0]
    digits[8] = get_by_length(row, 7)[0]

    # 7 has one segment (a) 1 does not have
    segments["a"] = get_diff(digits[7], digits[1])
    # 0,6,9 are all 6 digits but only 6 contains 1
    guess09 = []
    for guess069 in get_by_length(row, 6):
        if not set(digits[1]).issubset(set(guess069)):
            digits[6] = guess069
            # finding 6 we can also find f and c by comparing to 1
            segments["f"] = get_diff(digits[1], digits[6])
            segments["c"] = get_common(digits[1], digits[6])
        else:
            guess09.append(guess069)

    # now we tackle the 5 segments: 2, 3, 5
    guess235 = get_by_length(row, 5)

    # only 3 has c and f
    digits[3] = filter_contains(guess235, [segments["c"], segments["f"]])
    guess235.remove(digits[3])

    # 9 contains all of 3
    digits[9] = filter_contains(guess09, set(digits[3]))
    guess09.remove(digits[9])
    segments["e"] = get_diff(digits[8], digits[9])

    assert len(guess09) == 1
    digits[0] = guess09[0]

    # 2 and 5 remain, only 2 has e
    digits[2] = filter_contains(guess235, segments["e"])
    guess235.remove(digits[2])

    assert len(guess235) == 1
    digits[5] = guess235[0]

    res = list(range(10))
    for i in range(0, 10):
        res[i] = set(digits[i])
    return res


def partTwo(instr: str) -> int:

    l, r = parse(instr)
    ans = 0
    for i in range(len(l)):
        digits = decode(l[i])
        n = ""
        for val in r[i]:
            n += str(digits.index(set(val)))
        ans += int(n)
    return ans
