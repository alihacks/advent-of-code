
from typing import List
from copy import deepcopy

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 35
        self.test2 = 46

    def parse(self, instr: str) -> List:
        self.seeds, *self.maps = instr.split("\n\n")
        self.seeds =  [int(n) for n in self.seeds.split(": ")[1].split()]
        self.maps = [m.splitlines()[1:] for m in self.maps]
        self.maps = [[list(map(int,n.split())) for n in m] for m in self.maps]

    def solve(self):
        seeds = deepcopy(self.seeds)
        # Construct list of (delta, src range)
        map_ranges = [[(dst_start - src_start, range(src_start, src_start + rlen)) for dst_start, src_start, rlen in m] for m in self.maps]

        for ranges in map_ranges:
            for i in range(len(seeds)):
                seed = seeds[i]
                for delta, src in ranges:
                    if seed in src:
                        seeds[i] = seed + delta
                        break
        self.part1 = min(seeds)

        seeds = [range(self.seeds[i], self.seeds[i] + self.seeds[i+1]) for i in range(0,len(self.seeds),2)]
        for ranges in map_ranges:
            new_seeds = []
            for s in seeds:
                range_matched = False
                for delta, src in ranges:
                    overlap_start = max(src.start, s.start)
                    overlap_end = min(src.stop, s.stop)
                    if overlap_start >= overlap_end: # no overlap
                        continue
                    if s.start < overlap_start: #chunk before overlap
                        seeds.append(range(s.start, overlap_start))
                    if overlap_end < s.stop: #chunk after overlap
                        seeds.append(range(overlap_end, s.stop))
                    n = delta
                    new_seeds.append(range(overlap_start + n, overlap_end + n))
                    range_matched = True
                    break
                if not range_matched:
                    new_seeds.append(s)
            seeds = new_seeds
            
        self.part2 = min([s.start for s in seeds])