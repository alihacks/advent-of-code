from typing import List
import heapq


class Game:
    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    cols = {"A": 0, "B": 1, "C": 2, "D": 3}

    def indices(self):
        res = []
        for i in range(11):
            res.append([0, i])
        for i in range(1, len(self.g)):
            for j in range(4):
                res.append([i, j])
        return res

    def __init__(self, state):
        self.g = [list(state[0:11])]
        i = 11
        while i < len(state):
            self.g.append(list(state[i : i + 4]))
            i += 4

    def __str__(self):
        res = "".join(self.g[0]) + "\n"
        for i in range(1, len(self.g)):
            res += " |" + "|".join(self.g[i]) + "|\n"
        return res

    def get_state(self):
        state = ""
        for part in self.g:
            state += "".join(part)
        return state

    def room_ok(self, room):
        return all(
            [
                i == "." or Game.cols[i] == room
                for i in [self.g[j][room] for j in range(1, len(self.g))]
            ]
        )

    def moves(self, r, c):
        hallway_start = r == 0
        v = self.g[r][c]
        cr, cc = r, c
        m = []
        cost = Game.costs[v]
        current_cost = 0

        # in correct room, stay
        if r > 0 and Game.cols[v] == cc and self.room_ok(c):
            return []

        # get up in room
        while cr > 1:
            # if cr == 2:
            if self.g[r - 1][c] != ".":
                # print("stuck")
                return []
            cr -= 1
            current_cost += cost
            # m.append([cr, cc, current_cost])

        # into hallway
        if cr == 1:
            if self.g[cr - 1][cc * 2 + 2] != ".":
                # print("stuck")
                return []
            cr = cr - 1
            cc = cc * 2 + 2
            current_cost += cost
            m.append([cr, cc, current_cost])

        for lmove in range(1, cc + 1):
            # print("move left", lmove, "to", cc - lmove)
            if self.g[cr][cc - lmove] != ".":
                # print("blocked")
                break
            m.append([cr, cc - lmove, current_cost + lmove * cost])

        for rmove in range(1, 11 - cc):
            # print("move right", "to", rmove, cc + rmove)
            if self.g[cr][cc + rmove] != ".":
                # print("blocked")
                break
            m.append([cr, cc + rmove, current_cost + rmove * cost])

        # Down moves from hallway
        for r0, c0, cst in m:
            if r0 == 0 and c0 in [2, 4, 6, 8]:
                new_c = (c0 - 2) // 2
                if Game.cols[v] == new_c and self.room_ok(new_c):
                    rd = r0
                    # move down all the way you can
                    while rd + 1 < len(self.g):
                        if self.g[rd + 1][new_c] == ".":
                            rd += 1
                        else:
                            break
                    if rd != r0:
                        m.append([rd, new_c, cst + cost * rd])

        res = []
        for r0, c0, cst in m:
            if r0 == 0 and c0 in [2, 4, 6, 8]:
                continue
            if not hallway_start or (hallway_start and r0 != 0):
                res.append([r0, c0, cst])
        return res

    def next_games(self):
        res = []
        for r, c in self.indices():
            if self.g[r][c] == ".":
                continue
            for new_r, new_c, new_cost in self.moves(r, c):
                new_game = Game(self.get_state())
                new_game.g[r][c] = "."
                new_game.g[new_r][new_c] = self.g[r][c]
                res.append([new_game, new_cost])
        return res


class Solver:
    def __init__(self, input, is_test):
        self.parse(input)
        self.is_test = is_test
        self.test1 = 12521
        self.test2 = 44169

    def parse(self, instr):
        lines = instr.splitlines()
        state = lines[1][1:12]
        for i in [2, 3]:
            state += lines[i].replace("#", "").strip()
        self.init = Game(state)

    def least_energy(self):
        costs = {}
        q = [(0, self.init.get_state())]

        while q:
            cost, game_str = heapq.heappop(q)
            game = Game(game_str)

            for next_game, next_cost in game.next_games():
                next_state = next_game.get_state()
                total_cost = cost + next_cost
                if next_state in costs:
                    if total_cost < costs[next_state]:
                        costs[next_state] = total_cost
                        heapq.heappush(q, (total_cost, next_state))
                else:
                    costs[next_state] = total_cost
                    heapq.heappush(q, (total_cost, next_state))

        for key in costs:
            if key.startswith("." * 11):
                return costs[key]

    def solve(self):
        self.part1 = self.least_energy()
        state = self.init.get_state()
        self.init = Game(state[:15] + "DCBADBAC" + state[15:])
        self.part2 = self.least_energy()
