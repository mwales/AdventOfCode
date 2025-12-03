#!/usr/bin/env python3

import sys

def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")


def isValidId(curVal):

    curValStr = str(curVal)
    if len(curValStr) == 1:
        return False

    for chunkSize in range(1, len(curValStr) // 2 + 1):
        if len(curValStr) % chunkSize:
            continue

        #debug(f"Checking {curVal} in chunk size {chunkSize}")

        firstPart = curValStr[:chunkSize]
        numRepeats = len(curValStr) // chunkSize
        repeatedString = firstPart * numRepeats
        if repeatedString == curValStr:
            debug(f"Found {repeatedString}")
            return True

    return False

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


    print(f"Part 2 = {part1Sum}")

if __name__ == "__main__":
    main(sys.argv)
