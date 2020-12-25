from typing import List


def parse(instr: str) -> List:
    nums = [int(l) for l in instr.splitlines()]
    return nums


def partOne(instr: str) -> int:
    nums = parse(instr)
    loops = [0, 0]
    subj = 7
    t = 1
    lc = 0
    while 0  in loops:
        lc += 1
        t = (t * subj) % 20201227
        if t in nums:
            loops[nums.index(t)] = lc

    ans = 1
    subj = nums[1]
    for _ in range(loops[0]):
        ans = (ans * subj) % 20201227

    return ans


def partTwo(instr: str) -> int:
    input = parse(instr)
    return 0
