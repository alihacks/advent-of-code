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


def find_dest(lookup: dict, removed, cv: int, max: int) -> Cup:
    rnums = [removed.val, removed.next.val, removed.next.next.val]
    n = 3
    target = cv - 1
    for _ in range(n):
        if target in rnums:
            target -= 1

    # Couldn't find smaller, find largest
    if target <= 0:
        target = max  # max
        for _ in range(n):
            if target in rnums:
                target -= 1
    return lookup[target]


def pop3(current_cup: Cup):
    a = current_cup.next
    c = a.next.next
    current_cup.next = c.next
    return a

def make_ring(input):
    lookup = {}
    first_cup = None
    prev_cup = None
    for ci in input:
        new_cup = Cup(ci)
        lookup[ci] = new_cup
        if first_cup is None:
            first_cup = new_cup
        if not prev_cup is None:
            prev_cup.next = new_cup
        prev_cup = new_cup
    prev_cup.next = first_cup  # Complete the circle!!!
    return lookup, first_cup

def partOne(instr: str) -> int:
    debug = False
    iters = 100
    input = parse(instr)
    lookup, current_cup = make_ring(input)
    max = len(lookup)

    for i in range(iters):
        cv = current_cup.val
        if debug:
            print(f"-- Move {i+1} --\nCup: {current_cup}, current: {cv} ")
        removed = pop3(current_cup)
        if debug:
            print(f"Picked up: {removed}, cup: {current_cup} ")
        dest = find_dest(lookup, removed, cv, max)
        tn = dest.next
        dest.next = removed
        removed.next.next.next = tn

        current_cup = current_cup.next

    current_cup = lookup[1].next
    ans = ''
    while True:
        ans += str(current_cup.val)
        current_cup = current_cup.next
        if current_cup.val == 1:
            break

    return ans


def partTwo(instr: str) -> int:
    debug = False
    iters = 10000000
    input = parse(instr)

    # Add cups
    for m in range(max(input) + 1, 1000000 + 1):
        input.append(m)
    
    lookup, current_cup = make_ring(input)
    maxv = len(lookup)

    for i in range(iters):
        cv = current_cup.val
        if debug:
            print(f"-- Move {i+1} --\nCup: {current_cup}, current: {cv} ")
        removed = pop3(current_cup)
        if debug:
            print(f"Picked up: {removed}, cup: {current_cup} ")
        dest = find_dest(lookup, removed, cv, maxv)
        tn = dest.next
        dest.next = removed
        removed.next.next.next = tn

        current_cup = current_cup.next
    if debug:
        print(f"Final: {cup}")

    one_cup = lookup[1]
    return one_cup.next.val * one_cup.next.next.val
