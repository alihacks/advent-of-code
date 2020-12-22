from typing import List
from collections import deque
import copy


def parse(instr: str) -> List:
    chunks = instr.split('\n\n')
    players = []
    for chunk in chunks:
        l = []
        for num in chunk.strip().split('\n'):
            if not num.startswith('Player'):
                l.append(int(num))
        players.append(l)
    return players


def play1(p1: deque, p2: deque):
    while len(p1) > 0 and len(p2) > 0:
        c1 = p1.popleft()
        c2 = p2.popleft()
        #print(f"Playing {c1} vs {c2}")
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)


def calc_score(hand: deque):
    winner = copy.deepcopy(hand)
    winner.reverse()
    ans = 0
    for i in range(len(winner)):
        ans += winner[i] * (i + 1)
    return ans


def get_winner(p1: deque, p2: deque):
    if (len(p1) > 0):
        return(calc_score(p1))
    else:
        return(calc_score(p2))


def partOne(instr: str) -> int:
    players = parse(instr)
    p1 = deque(players[0])
    p2 = deque(players[1])
    play1(p1, p2)
    return(get_winner(p1, p2))


def play2(p1: deque, p2: deque, game=1, debug=False):
    round = 1
    seen = set()
    if debug:
        print(f"{'---'*10} Game {'---'*10}")
    while len(p1) > 0 and len(p2) > 0:
        h_check = (tuple(p1), tuple(p2))
        if (h_check in seen):
            return 1  # loop detected
        seen.add(h_check)

        if debug:
            print(f"Game {game}, Round {round}: {p1} {p2}")
        c1 = p1.popleft()
        c2 = p2.popleft()
        if debug:
            print(f"Playing {c1} vs {c2}")
        round += 1
        # If both players have at least as many cards remaining in their deck as the value of the card they just drew,
        # the winner of the round is determined by playing a new game of Recursive Combat
        if len(p1) >= c1 and len(p2) >= c2:
            #print("Playing a sub-game to determine the winner...")
            copy1 = deque(list(p1)[:c1])
            copy2 = deque(list(p2)[:c2])
            #print(f"Recurse with {copy1}  {copy2}")

            winner = play2(copy1, copy2, game + 1)
            if winner == 1:
                p1.append(c1)
                p1.append(c2)
            else:  # 2 won
                p2.append(c2)
                p2.append(c1)
        else:
            # Otherwise, at least one player must not have enough cards left in their deck to recurse
            # the winner of the round is the player with the higher-value card.
            if c1 > c2:
                if debug:
                    print("P1 wins")
                p1.append(c1)
                p1.append(c2)
            else:
                if debug:
                    print("P2 wins")
                p2.append(c2)
                p2.append(c1)
    if len(p1) > 0:
        return 1
    return 2


def partTwo(instr: str) -> int:
    players = parse(instr)
    p1 = deque(players[0])
    p2 = deque(players[1])
    play2(p1, p2)
    return(get_winner(p1, p2))
