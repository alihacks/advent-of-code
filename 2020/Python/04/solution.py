from typing import List
import re


def parse(instr: str) -> List:
    passports = []
    current = {}
    for line in instr.splitlines():
        if not line and current:  # break, add what we have
            passports.append(current)
            current = {}
        else:
            line_vals = line.split(' ')
            for val in line_vals:
                k, v = val.split(':')
                current[k] = v
    # Add last passport
    passports.append(current)
    return passports


def check_fields(passport):
    fields = set(passport.keys())
    fields.discard('cid')
    return fields == {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}


def partOne(instr: str) -> int:
    input = parse(instr)
    cnt = 0
    for passport in input:
        if (check_fields(passport)):
            cnt += 1
    return cnt


def check_num(value: str, min: int, max: int):
    if value.isdigit():
        return min <= int(value) <= max
    return False


def check_hgt(value: str):
    units = value[-2:]
    hgt = value[:-2]
    if units == "cm":
        return check_num(hgt, 150, 193)
    elif units == "in":
        return check_num(hgt, 59, 76)
    return False


def partTwo(instr: str) -> int:
    input = parse(instr)
    cnt = 0
    for passport in input:
        if not check_fields(passport):
            continue
        if not check_num(passport['byr'], 1920, 2002):
            continue
        if not check_num(passport['iyr'], 2010, 2020):
            continue
        if not check_num(passport['eyr'], 2020, 2030):
            continue
        if not re.search("^#[0-9a-f]{6}$", passport['hcl']):
            continue
        if not check_hgt(passport['hgt']):
            continue
        if not passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            continue
        if not re.search("^[0-9]{9}$", passport['pid']):
            continue
        cnt += 1
    return cnt
