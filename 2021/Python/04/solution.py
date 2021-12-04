from typing import List


class BingoBoard:
    def __init__(self, input_string, idx):
        self.idx = idx
        # storing rows and cols separately to easily check for BINGO
        self.rows = [set() for _ in range(5)]
        self.cols = [set() for _ in range(5)]

        lines = input_string.split("\n")
        for r in range(5):  # no error checking here, assuming 5
            nums = list(map(int, lines[r].split()))
            for c in range(5):
                self.rows[r].add(nums[c])
                self.cols[c].add(nums[c])

    def play(self, num) -> bool:  # return true if BINGO
        is_bingo = False
        for i in range(5):
            self.rows[i].discard(num)
            self.cols[i].discard(num)
            if len(self.rows[i]) == 0 or len(self.cols[i]) == 0:
                is_bingo = True
        return is_bingo

    def get_sum(self) -> int:
        return sum([sum(self.rows[i]) for i in range(5)])


def parse(instr: str):
    boards = []
    parts = instr.split("\n\n")
    nums = list(map(int, parts[0].split(",")))
    board_input = parts[1::]
    b_idx = 1
    for bi in board_input:
        boards.append(BingoBoard(bi, b_idx))
        b_idx = b_idx + 1
    return nums, boards


def partOne(instr: str) -> int:
    nums, boards = parse(instr)
    for num in nums:
        for board in boards:
            is_bingo = board.play(num)
            if is_bingo:
                return num * board.get_sum()


def partTwo(instr: str) -> int:
    nums, boards = parse(instr)
    winners = set()
    last_winner = 0
    for num in nums:
        if len(winners) == len(boards):
            break
        for board in boards:
            if board.idx in winners:
                continue
            is_bingo = board.play(num)
            if is_bingo:
                winners.add(board.idx)
                last_winner = board.get_sum() * num
    return last_winner
