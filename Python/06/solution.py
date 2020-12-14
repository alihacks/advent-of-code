from typing import List


def parse(instr: str) -> List:
    forms = []
    current = []
    for line in instr.splitlines():
        if not line:  # break, add what we have
            forms.append(current)
            current = []
        else:
            current.append(line)
    # Add last form
    forms.append(current)
    return forms


def partOne(instr: str) -> int:
    forms = parse(instr)
    cnt = 0
    for form in forms:
        form_set = set()
        for answer in form:
            form_set = form_set.union(set(answer))
        cnt += len(form_set)
    return cnt


def partTwo(instr: str) -> int:
    forms = parse(instr)
    cnt = 0
    for form in forms:
        if len(form) > 0:
            form_set = set(form[0])
            for answer in form:
                form_set = form_set.intersection(set(answer))
            cnt += len(form_set)
    return cnt
