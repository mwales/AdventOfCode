#!/usr/bin/env python3

import sys

def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

def isValidId(curVal):
    curValStr = str(curVal)
    if len(curValStr) % 2:
        return False

    centerPoint = len(curValStr) // 2
    part1 = curValStr[:centerPoint]
    part2 = curValStr[centerPoint:]
    return (part1 == part2)


def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    part1Sum = 0
    for singleRange in data[0].split(","):
        parts = singleRange.split("-")
        firstNum = int(parts[0])
        secondNum = int(parts[1])

        for valueToCheck in range(firstNum, secondNum + 1):
            if (isValidId(valueToCheck)):
                part1Sum += valueToCheck


    print(f"Part 1 = {part1Sum}")

if __name__ == "__main__":
    main(sys.argv)
