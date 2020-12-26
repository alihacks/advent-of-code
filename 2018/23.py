from aocd import lines, get as aocd_get

# Test
puzzle_day, puzzle_year = aocd_get.get_day_and_year()
#lines = open(f"./{puzzle_day}.test.txt").read().splitlines()


def calc_md(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])


bots = []
for l in lines:
    [pos, rpart] = l.replace('pos=<', '').split('>')
    rpart = int(rpart.split('=')[1])
    coords = [int(i) for i in pos.split(',')]
    bots.append(tuple([rpart, coords]))

bc = len(bots)
max_r = max([i[0] for i in bots])
maxbot = next(b for b in bots if b[0] == max_r)
maxloc = maxbot[1]
ans = 0
for r, coords in bots:
    md = calc_md(maxloc, coords)
    if md <= max_r:
        ans += 1

print("Part1:", ans)


def bron_kerbosch(r: set, p: set, x: set, best_r: set):
    #print(r, p, x)
    if not p and not x:
        if len(r) > len(best_r):
            best_r.clear()
            best_r.update(r)
    px = p | x
    max_n = 0
    max_ni = 0
    for i in px:
        if bots[i][3] > max_n:
            max_n = bots[i][3]
            max_ni = i
    for bot_i in p:
        if bot_i in bots[max_ni][2]:
            continue
        neighbors = bots[bot_i][2]
        bron_kerbosch(r.union({bot_i}), p.intersection(neighbors),
                      x.intersection(neighbors), best_r)
    return best_r


for i in range(bc):
    r, coords = bots[i]
    overlaps = set()
    for j in range(bc):
        if i == j:
            continue
        r2, c2, *_ = bots[j]
        if calc_md(coords, c2) <= r + r2:  # circles overlap
            overlaps.add(j)
    bots[i] = (r, coords, overlaps, len(overlaps))


p = set(range(bc))
best_r = set()
bron_kerbosch(set(), p, set(), best_r)

max_md = 0
for i in best_r:
    r, c, *_ = bots[i]
    val = calc_md([0, 0, 0], c) - r
    if val > max_md:
        max_md = val
print(max_md)
assert max_md == 93130765
print("Part2:", max_md)
