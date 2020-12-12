import json
import platform
import sys
import pathlib

from rich import print

from solution import partOne, partTwo


if __name__ == "__main__":

    year = "2020"
    day = pathlib.Path(__file__).parent.name

    print(f"[yellow]AoC {year}[/yellow]: Day {day}")
    print(f"Python {platform.python_version()}\n")

    try:
        test_input = open("test.txt").read()
        print("Part 1 Test:", partOne(test_input))
        print("Part 2 Test:", partTwo(test_input))
    except FileNotFoundError:
        print("Info: Skipping tests, test.txt not found")

    if "debug" in sys.argv:
        sys.exit()

    try:
        challenge_input = open("input.txt").read()
    except FileNotFoundError:
        print("Error: could not open input.txt")
        sys.exit(-1)

    print("Answers")
    print("Part 1:", partOne(challenge_input))
    print("Part 2:", partTwo(challenge_input))
