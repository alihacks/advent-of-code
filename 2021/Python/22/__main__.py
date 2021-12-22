import platform
import sys
import pathlib
import os

# from rich import print
from solver import Solver


if __name__ == "__main__":

    year = "2021"
    day = pathlib.Path(__file__).parent.name
    dir = pathlib.Path(__file__).parent.absolute()

    ICON_PASS = "\U00002705"
    ICON_FAIL = "\U0000274C"

    print(f"[yellow]AoC {year}[/yellow]: Day {day}")
    print(f"Python {platform.python_version()}\n")

    try:
        test_input = open(os.path.join(dir, "test.txt")).read()
        s = Solver(test_input, True)
        s.solve()
        print(
            "Part 1 Test:",
            s.part1,
            ICON_PASS
            if s.part1 == s.test1
            else ICON_FAIL + " (!= " + str(s.test1) + ")",
        )
        test_input = open(os.path.join(dir, "test2.txt")).read()
        s = Solver(test_input, True)
        s.solve()
        print(
            "Part 2 Test:",
            s.part2,
            ICON_PASS
            if s.part2 == s.test2
            else ICON_FAIL + " (!= " + str(s.test2) + ")",
        )
    except FileNotFoundError:
        print("Info: Skipping tests, test.txt not found")

    if "debug" in sys.argv:
        sys.exit()

    try:
        challenge_input = open(os.path.join(dir, "input.txt")).read()
    except FileNotFoundError:
        print("Error: could not open input.txt")
        sys.exit(-1)

    print("Answers")
    s = Solver(challenge_input, False)
    s.solve()
    print("Part 1:", s.part1)
    print("Part 2:", s.part2)
