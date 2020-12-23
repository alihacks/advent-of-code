from typing import List


def parse(instr: str) -> List:
    return list([int(i) for i in instr.splitlines()[0]])


class Cup:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        nv = "(null)"
        if not self.next is None:
            nv = str(self.next.val)
        return f"Cup: {self.val} -> {nv}"


def find_dest(lookup: list, removed: list, cv: int) -> Cup:
    rnums = [i.val for i in removed]
    target = cv - 1
    for _ in range(len(removed)):
        if target in rnums:
            target -= 1

    # Couldn't find smaller, find largest
    if target <= 0:
        target = len(lookup) - 1  # max
        for _ in range(len(removed)):
            if target in rnums:
                target -= 1
    return lookup[target]


def pop3(current_cup: Cup):
    a = current_cup.next
    b = a.next
    c = b.next
    current_cup.next = c.next
    return [a, b, c]


def partOne(instr: str) -> int:
    debug = False
    input = parse(instr)
    cup_count = len(input)
    lookup = [None for _ in range(cup_count + 1)]

    first_cup = None
    prev_cup = None
    for ci in input:
        new_cup = Cup(ci)
        if first_cup is None:
            first_cup = new_cup
        if not prev_cup is None:
            prev_cup.next = new_cup
        prev_cup = new_cup
    prev_cup.next = first_cup  # Complete the circle!!!

    current_cup = first_cup.next
    lookup[first_cup.val] = first_cup
    while current_cup != first_cup:
        lookup[current_cup.val] = current_cup
        current_cup = current_cup.next

    iters = 100

    current_cup = first_cup
    for i in range(iters):
        cv = current_cup.val
        if debug:
            print(f"-- Move {i+1} --\nCup: {current_cup}, current: {cv} ")
        removed = pop3(current_cup)
        if debug:
            print(f"Picked up: {removed}, cup: {current_cup} ")
        dest = find_dest(lookup, removed, cv)
        tn = dest.next
        dest.next = removed[0]
        removed[-1].next = tn

        current_cup = current_cup.next

    one_cup = first_cup
    while True:
        if one_cup.val == 1:
            break
        one_cup = one_cup.next
    current_cup = one_cup.next
    ans = ''
    while True:
        ans += str(current_cup.val)
        current_cup = current_cup.next
        if current_cup.val == 1:
            break

    return ans


def partTwo(instr: str) -> int:
    debug = False
    input = parse(instr)

    # Add cups
    m = max(input) + 1
    while m <= 1000000:
        input.append(m)
        m += 1

    cup_count = len(input)
    lookup = [None for _ in range(cup_count + 1)]

    first_cup = None
    prev_cup = None
    for ci in input:
        new_cup = Cup(ci)
        if first_cup is None:
            first_cup = new_cup
        if not prev_cup is None:
            prev_cup.next = new_cup
        prev_cup = new_cup
    prev_cup.next = first_cup  # Complete the circle!!!

    current_cup = first_cup.next
    lookup[first_cup.val] = first_cup
    while current_cup != first_cup:
        lookup[current_cup.val] = current_cup
        current_cup = current_cup.next

    iters = 10000000

    current_cup = first_cup
    for i in range(iters):
        cv = current_cup.val
        if debug:
            print(f"-- Move {i+1} --\nCup: {current_cup}, current: {cv} ")
        removed = pop3(current_cup)
        if debug:
            print(f"Picked up: {removed}, cup: {current_cup} ")
        dest = find_dest(lookup, removed, cv)
        tn = dest.next
        dest.next = removed[0]
        removed[-1].next = tn

        current_cup = current_cup.next
    if debug:
        print(f"Final: {cup}")

    one_cup = first_cup
    while True:
        if one_cup.val == 1:
            break
        one_cup = one_cup.next

    return one_cup.next.val * one_cup.next.next.val
