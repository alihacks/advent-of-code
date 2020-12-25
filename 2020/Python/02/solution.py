from typing import List


def parse(instr: str) -> List:
    return [
        line
        for line in instr.splitlines()
    ]


def partOne(instr: str) -> int:
    input_list = parse(instr)
    cnt = 0
    for rule in input_list:
        num_range, letter, password = rule.split(' ')
        letter = letter[0]  # remove :
        min_count, max_count = map(int, num_range.split('-'))
        if max_count >= password.count(letter) >= min_count:
            cnt += 1
    return cnt


def partTwo(instr: str) -> int:
    input_list = parse(instr)
    cnt = 0
    for rule in input_list:
        num_range, letter, password = rule.split(' ')
        letter = letter[0]  # remove :
        pos1, pos2 = map(lambda x: int(x) - 1, num_range.split('-'))  # 0 base
        check1 = password[pos1] == letter
        check2 = password[pos2] == letter
        if check1 ^ check2:
            cnt += 1
    return cnt
