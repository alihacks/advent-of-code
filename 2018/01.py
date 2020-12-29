from aocd import lines, get as aocd_get

# Test
puzzle_day, puzzle_year = aocd_get.get_day_and_year()
# lines = open(f"./{puzzle_day}.test.txt").read().splitlines()

ans = 0
seen = {ans}
found = 0

for line in lines:
    ans += int(line)
    if ans in seen:
        found = ans
        break
    seen.add(ans)

print("Part1:", ans)

while not found:
    for line in lines:
        ans += int(line)
        if ans in seen:
            found = ans
            break
        seen.add(ans)

print("Part2:", found)
