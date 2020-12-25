from typing import List


def parse(instr: str) -> List:
    rules = {}
    tickets = []
    mode = 'rules'
    for line in instr.splitlines():
        if mode == 'rules':
            if not line:
                mode = 'my'
                continue
            rule_name, vals = line.split(':')
            ranges = vals.strip().split(' or ')
            ranges = [[int(n) for n in rule.split('-')] for rule in ranges]
            rules.update({rule_name: ranges})
        elif mode == 'my':
            if not line:
                mode = 'tickets'
                continue
            elif line == 'your ticket:':
                continue
            my_ticket = [int(n) for n in line.split(',')]
        else:
            if line == 'nearby tickets:':
                continue
            tickets.append([int(n) for n in line.split(',')])
    return rules, my_ticket, tickets


def partOne(instr: str) -> int:
    rules, _, tickets = parse(instr)
    invalid_sum = 0
    for t in tickets:
        for val in t:
            valid = False
            for rule in rules:
                for ranges in rules[rule]:
                    if ranges[0] <= val <= ranges[1]:
                        valid = True
                        break
                if valid:
                    break
            if not valid:
                invalid_sum += val

    return invalid_sum


def getValidTickets(rules, tickets):
    valid_tickets = []
    potentials = []
    for t in tickets:
        ticket_valid = True
        pot = []
        i = 0
        for val in t:
            valid = False
            pot.append([])
            for rule in rules:
                for ranges in rules[rule]:
                    if ranges[0] <= val <= ranges[1]:
                        valid = True
                        pot[i].append(rule)
            if not valid:
                ticket_valid = False
            i += 1
        if ticket_valid:
            valid_tickets.append(t)
            potentials.append(pot)
    return valid_tickets, potentials


def partTwo(instr: str) -> int:
    rules, my_ticket, tickets = parse(instr)
    _, potentials = getValidTickets(rules, tickets)
    found_list = []
    final_list = {}
    for i in range(0, len(potentials[0])):
        found = []
        for row in potentials:
            if not found:
                found = set(row[i])
            else:
                found = found.intersection(row[i])
        found_list.append(list(found))

    # Process of elimination for cols
    progress = True
    while progress:
        progress = False
        for i in range(0, len(found_list)):
            f = found_list[i]
            if (len(f) == 1):  # unique solution
                progress = True
                found_item = f[0]
                f.remove(found_item)
                final_list.update({i: found_item})
                for f2 in found_list:
                    if (found_item in f2):
                        f2.remove(found_item)
                break

    ans = 1
    for i in final_list:
        if final_list[i].startswith('departure'):
            ans *= my_ticket[i]
    return ans
