from typing import List
import itertools, math
import networkx as nx

class Solver:
    def __init__(self, input_str, is_test: bool):
        self.is_test = is_test
        self.parse(input_str)
        self.part1, self.part2 = 0, 0
        self.test1 = 40
        self.test2 = 25272

    def parse(self, instr: str) -> List:
        self.data = [tuple(map(int,line.split(','))) for line in instr.splitlines()]

    def solve(self):
        distances = []
        for p1, p2 in itertools.combinations(self.data, 2):
            d = math.dist(p1, p2)
            distances.append((d,p1,p2))
        distances.sort(key=lambda x: x[0])
        tdist = distances[:10 if self.is_test else 1000]
        G = nx.Graph()
        G.add_edges_from([(p1, p2) for _,p1, p2 in tdist])
        g = list(nx.connected_components(G))
        lens = [len(grp) for grp in g]
        lens.sort(reverse=True)
        self.part1 = math.prod(lens[:3])

        G = nx.Graph()
        for d, p1, p2 in distances:
            G.add_edge(p1, p2, weight=d)
        mst = list(nx.minimum_spanning_tree(G).edges(data=True))
        mst.sort(key=lambda x: x[2]['weight'])
        last = mst[-1]
        self.part2 = last[0][0] * last[1][0]



