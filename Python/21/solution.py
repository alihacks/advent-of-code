from typing import List


def parse(instr: str) -> List:
    data = []
    for line in instr.splitlines():
        [l, c] = line.replace(')', '').split(' (contains ')
        ings = l.split(' ')
        conts = c.split(', ')
        data.append((ings, conts))
    return data


def get_allergens(input):
    allergens = {}
    i_set = set()
    i_list = []
    for item in input:
        ings, conts = item
        i_set |= set(ings)
        i_list += ings
        for allergen in conts:
            if allergen not in allergens:
                allergens.update({allergen: set(ings)})
            else:
                allergens[allergen] = allergens[allergen] & set(ings)
    return allergens, i_set, i_list


def partOne(instr: str) -> int:
    input = parse(instr)
    allergens, i_set, i_list = get_allergens(input)
    a_set = set()
    for k, v in allergens.items():
        a_set |= v

    non_allergens = [x for x in i_list if x not in a_set]
    return len(non_allergens)


def partTwo(instr: str) -> int:
    input = parse(instr)
    allergens, _, _ = get_allergens(input)
    translated = {}
    progress = True
    while progress:
        progress = False
        for k, v in allergens.items():
            if len(v) == 1:  # definitive match
                progress = True
                match = v.pop()
                translated.update({k: match})
                for k1, v1 in allergens.items():
                    if match in v1:
                        v1.remove(match)
    # canonical sort
    ans = ",".join([translated[k] for k in sorted(translated)])
    return ans
