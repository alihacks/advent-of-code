from typing import List


def parse(instr: str) -> List:
    return [
        line
        for line in instr.splitlines()
    ]


def get_seat_id(ticket: str):
    row = int(ticket[:7].replace('B', '1').replace('F', '0'), 2)
    col = int(ticket[7:].replace('R', '1').replace('L', '0'), 2)
    return row * 8 + col


def partOne(instr: str) -> int:
    input = parse(instr)
    answer = 0
    for ticket in input:
        answer = max(answer, get_seat_id(ticket))
    return answer


def partTwo(instr: str) -> int:
    input = parse(instr)
    seats = []
    for ticket in input:
        seats.append(get_seat_id(ticket))
    return set(range(min(seats), max(seats))).difference(set(seats)).pop()
