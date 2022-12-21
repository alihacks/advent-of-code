from typing import List
import re, math, z3

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.parse(input_str)
        self.is_test = is_test
        self.part1, self.part2 = 0, 0
        self.test1 = 33
        self.test2 = 56 * 62

    def parse(self, instr: str) -> List:
        self.data = [list(map(int,re.findall(r'\d+',line))) for line in instr.splitlines()]

    def maximize(self, bp, time):
        geodes = 0
        z = z3.Optimize()
        _, ore_cost, clay_cost, obs_cost_ore, obs_cost_clay, geode_cost_ore, geode_cost_obs =  bp
        t = [] # time array of vars
        for ti in range(time+1):
            d = {}
            for var in ['ore','clay','obs','ore_robots','clay_robots','obs_robots']:
                d[var] = z3.Int(f'{var}_{ti}')
            for var in ['build_ore', 'build_clay','build_obs','build_geode']:
                d[var] = z3.Bool(f'{var}_{ti}')
            t.append(d)

        z.add(t[0]['ore'] == 0)
        z.add(t[0]['clay'] == 0)
        z.add(t[0]['obs'] == 0)
        z.add(t[0]['ore_robots'] == 1)
        z.add(t[0]['clay_robots'] == 0)
        z.add(t[0]['obs_robots'] == 0)

        for ti in range(time):
            v = t[ti]
            if ti > 0:
                v0 = t[ti - 1]
                # budgeting
                ore_spend = v0['build_ore'] * ore_cost + v0['build_clay'] * clay_cost + v0['build_obs'] * obs_cost_ore + v0['build_geode'] * geode_cost_ore
                clay_spend = v0['build_obs'] * obs_cost_clay
                obs_spend = v0['build_geode'] * geode_cost_obs

                z.add(v['ore']  == v0['ore'] + v0['ore_robots'] - ore_spend)
                z.add(v['clay'] == v0['clay'] + v0['clay_robots'] - clay_spend)
                z.add(v['obs'] == v0['obs'] + v0['obs_robots'] - obs_spend)

                z.add(v['ore_robots'] == v0['ore_robots'] + v0['build_ore'])
                z.add(v['clay_robots'] == v0['clay_robots'] + v0['build_clay'])
                z.add(v['obs_robots'] == v0['obs_robots'] + v0['build_obs'])
            
            # Can build 1 robot at a time
            z.add( z3.PbLe([(x,1) for x in [v['build_ore'], v['build_clay'], v['build_obs'], v['build_geode']]],1) )

            # Check ore, clay, obs build possibilities
            z.add(v[f'build_ore'] * ore_cost <= v['ore'])
            z.add(v[f'build_clay'] * clay_cost <= v['ore'])
            z.add(v[f'build_obs'] * obs_cost_ore <= v['ore'])
            z.add(v[f'build_geode'] * geode_cost_ore <= v['ore'])
            z.add(v['build_obs'] * obs_cost_clay <= v['clay'])
            z.add(v['build_geode'] * geode_cost_obs <= v['obs'])

            geodes += v['build_geode'] * (time - ti - 1)

        sc = z.maximize(geodes)
        z.check()
        return sc.value().as_long()

    def solve(self):
        self.part1 = sum(bp[0] * self.maximize(bp, 24) for bp in self.data)
        self.part2 = math.prod(self.maximize(bp, 32) for bp in self.data[:3])
