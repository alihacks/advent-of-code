import collections
import functools
import operator
import itertools
import copy
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def main(input, is_real):
    template = "Step {} must be finished before step {} can begin."
    reqs = collections.defaultdict(set)
    for line in input:
        pre_step, step = parse(template, line)
        reqs[step].add(pre_step)
        if pre_step not in reqs:
            reqs[pre_step] = set()
    reqs0 = copy.deepcopy(reqs)
    ans = ""
    while reqs:
        next_step = min([k for k in reqs if not reqs[k]])
        ans += next_step
        del reqs[next_step]
        for _, v in reqs.items():
            if next_step in v:
                v.remove(next_step)

    print("Part1:", ans)
    reqs = reqs0
    cost = {}
    for c in range(ord('A'), ord('Z') + 1):
        cost[chr(c)] = c - ord('A') + (61 if is_real else 1)

    w = 5 if is_real else 2
    workers = [0 for _ in range(w)]
    worker_jobs = [None for _ in range(w)]

    seconds = 0
    while reqs:
        todo = [k for k in reqs if not reqs[k] and k not in worker_jobs]
        while 0 in workers and todo:
            i = workers.index(0)
            job = todo.pop(0)
            workers[i] = cost[job]
            worker_jobs[i] = job

        # Work the workers
        for i in [wi for wi in range(w) if workers[wi] > 0]:
            # Work it
            workers[i] -= 1
            if workers[i] == 0:  # job well done
                job = worker_jobs[i]
                worker_jobs[i] = None
                del reqs[job]
                for _, v in reqs.items():
                    if job in v:
                        v.remove(job)
        seconds += 1

    print("Part2:", seconds)


sample_input = r"""
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)
print("[green]Real:")
main(lines, True)
