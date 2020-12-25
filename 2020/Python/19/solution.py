from typing import List
import re


def parse(instr: str) -> List:
    is_rule = True
    rules = {}
    inputs = []
    for line in instr.splitlines():
        if is_rule:
            if not line:
                is_rule = False
                continue
            name, rule = line.replace('"', '').split(": ")
            rule_list = []
            for rulepart in rule.split(" | "):
                rule_list.append(rulepart.strip().split(' '))
            rules.update({name: rule_list})
        else:
            inputs.append(line)
    return rules, inputs


def check(rules, str, rid, d=0):
    r = rules[rid]
    # Assume char rules are singles (No "a" | "b")
    if 'a' <= r[0][0] <= 'z':
        # print(f"str: {str}")
        # print(f"try {r[0][0]} for {str}: {str[0] == r[0][0]}")
        if len(str) > 0 and str[0] == r[0][0]:
            return 1
        return 0
    found = [0] * len(r)
    for i in range(len(r)):  # part | part
        part = r[i]
        # print(f"Part {part} i={i} r={r} found={found}")
        found[i] = 0
        satisfied = 0
        delta = 0
        for j in range(len(part)):  # 1 2
            sub_rule = part[j]
            delta = check(rules, str[found[i]:], sub_rule, d + 1)
            found[i] += delta
            if delta > 0:
                satisfied += 1

            # print("  " * d + f" i is now {i}")
        if satisfied != len(part):
            found[i] = 0
    # print(f"Found is {found}")
    return max(found)


def partOne(instr: str) -> int:

    rules, inputs = parse(instr)
    ans = 0
    for input in inputs:
        if check(rules, input, '0') == len(input):
            ans += 1
    return ans


def parse2(instr: str) -> List:
    is_rule = True
    rules = {}
    inputs = []
    for line in instr.splitlines():
        if is_rule:
            if not line:
                is_rule = False
                continue
            name, rule = line.replace('"', '').split(": ")
            pieces = rule.split(" | ")
            for p in range(len(pieces)):
                nums = pieces[p].split(' ')
                pieces[p] = ''.join([f'({n})' for n in nums])
            rule = "|".join(pieces)
            rules.update({name: rule})
        else:
            inputs.append(line)
    return rules, inputs


def apply_rule(rules, rule_no, val):
    for r in rules:
        rules[r] = rules[r].replace(f"({rule_no})", f"({val})")


def partTwo(instr: str) -> int:  # GIVE UP REGEX IT
    rules, inputs = parse2(instr)
    ans = 0

    rules['8'] += '+'

    s = []
    for i in range(1, 10):  # guess based on len
        s.append('(' + '(42)' * i + '(31)' * i + ')')
    rules['11'] = "|".join(s)

    for i in range(0, len(rules)):
        for r in rules:
            rule = rules[r]
            if not re.match(".*[0-9].*", rule):  # rule is letters
                apply_rule(rules, r, rule)

    exp = f"^{rules['0']}$"
    # print(exp)
    for line in inputs:
        if re.match(exp, line):
            ans += 1

    return ans
