from typing import List


def parse(instr: str) -> List:
    masks = []
    curmask = {}
    curmask['commands'] = []
    for line in instr.splitlines():
        if line.startswith('mask'):
            if len(curmask['commands']):
                masks.append(curmask)
                curmask = {}
                curmask['commands'] = []
            curmask['mask'] = line.replace('mask = ', '')
        else:
            memsets = line.replace(
                'mem[', '').replace(']', '').replace(' ', '')
            loc, val = memsets.split('=')
            curmask['commands'].append(tuple([loc, val]))
    # Add last
    masks.append(curmask)
    return masks


def partOne(instr: str) -> int:
    input = parse(instr)
    data = {}
    for chunk in input:
        mask = chunk['mask']
        imask = int(mask.replace('X', '0'), 2)
        realmask = mask.replace('0', '1').replace('X', '0')
        irealmask = int(realmask, 2)

        for cmd in chunk['commands']:
            loc, val = cmd
            if loc not in data:  # init new mem spot
                data.update({loc: 0})
            ival = int(val)
            ival &= ~irealmask
            ival |= imask
            data.update({loc: ival})

    return sum_data(data)


def sum_data(data: dict):
    sum = 0
    for entry in data:
        sum += data[entry]
    return sum


def get_magic(mask, loc):
    strloc = format(int(loc), '036b')
    for i in range(0, len(mask)):
        if mask[i] != '0':  # 0 does nothing
            l = list(strloc)
            l[i] = mask[i]
            strloc = "".join(l)
    return strloc


def magic_write(data, magicmask: str, val):
    if "X" not in magicmask:
        loc = int(magicmask, 2)
        data.update({loc: int(val)})
    else:  # Recursion baby!
        magic_write(data, magicmask.replace('X', '0', 1), val)
        magic_write(data, magicmask.replace('X', '1', 1), val)


def partTwo(instr: str) -> int:
    input = parse(instr)
    data = {}
    for chunk in input:
        mask = chunk['mask']
        for cmd in chunk['commands']:
            loc, val = cmd
            magicmask = get_magic(mask, loc)
            magic_write(data, magicmask, val)
    return sum_data(data)
