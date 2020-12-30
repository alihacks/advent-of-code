import collections
import functools
import operator
import itertools
import re
from parse import parse
from rich import print
from aocd import lines, get as aocd_get


def main(input, is_real):
    ts = "[{y:4d}-{m:2d}-{d:2d} {hr:2d}:{mn:2d}]"
    guard_template = ts + " Guard #{id:d} begins shift"
    event_template = ts + " {event}"
    input.sort()

    current_guard = 0
    sleep_start = 0
    guards = {}
    for line in input:
        # print(line)
        new_guard = parse(guard_template, line)
        if new_guard:
            current_guard = int(new_guard['id'])
            if not current_guard in guards:
                guards.update({current_guard: collections.Counter()})
        else:
            event = parse(event_template, line)
            if event['event'] == 'falls asleep':
                sleep_start = int(event['mn'])
            else:
                mn = int(event['mn'])
                guards[current_guard].update(
                    [i for i in range(sleep_start, mn)])

    sleep_mins = dict([(g, sum(c.values())) for g, c in guards.items()])
    sleepy_guard_id = max(sleep_mins, key=sleep_mins.get)

    sleepiest_min, _ = guards[sleepy_guard_id].most_common(1)[0]
    ans = sleepy_guard_id * sleepiest_min

    print("Part1:", ans)

    gm = [(g, next(iter(c.most_common(1)), None))
          for g, c in guards.items() if len(c) > 0]
    smid, (minute, _) = max(gm, key=lambda x: list(x[1])[1])
    print("Part2:", smid * minute)


sample_input = r"""
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""

sample_lines = sample_input.strip().splitlines()

print("[yellow]Sample:")
main(sample_lines, False)

print("[green]Real:")
main(lines, True)
