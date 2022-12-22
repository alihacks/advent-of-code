from typing import List
import re, sys
from collections import defaultdict

class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 1651
        self.test2 = 1707

    def parse(self, instr: str) -> List:
        self.valves = {}
        self.flow = {}
        for p in [re.findall(r'[A-Z]{2}|[0-9]+', line) for line in instr.splitlines()]:
            self.valves[p[0]] = set(p[2:])
            if int(p[1]) > 0:
                self.flow[p[0]] = int(p[1])
        self.states = {x: 1<<i for i, x in enumerate(self.flow)}
        

    def solve(self):
        path_costs = defaultdict(dict)
        for source in self.valves:
            for dest in self.valves:
                path_costs[source][dest] = 1 if dest in self.valves[source] else sys.maxsize

        for via in self.valves:
            for source in path_costs:
                for dest in path_costs:
                    potential_cost = path_costs[source][via]+path_costs[via][dest]
                    if potential_cost < path_costs[source][dest]:
                        path_costs[source][dest] = potential_cost


        def visit(valve, time_left, state, total_flow, max_flows):
            max_flows[state] = max(max_flows[state] if state in max_flows else 0, total_flow)
            for f in self.flow:
                new_time_left = time_left - path_costs[valve][f] - 1
                if self.states[f] & state or new_time_left < 0: continue
                visit(f, new_time_left, state | self.states[f], total_flow + new_time_left * self.flow[f], max_flows)
            return max_flows

        self.part1 = max(visit('AA', 30, 0, 0, {}).values())

        flows = visit('AA', 26, 0, 0, {})
        self.part2 = max([v + v2 for k, v in flows.items() 
                   for k2, v2 in flows.items() if not k & k2]) # must open different valves