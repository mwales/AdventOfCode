#!/usr/bin/env python3

import sys

def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

def findPeakJolt(valStr):
    maxFirst = 0
    curMax = 0
    
    for firstDigitPos in range(len(valStr) - 1):
        curFD = int(valStr[firstDigitPos])
        if (curFD < maxFirst):
            continue

        for secondDigitPos in range(firstDigitPos + 1, len(valStr)):
            curSD = int(valStr[secondDigitPos])

            curVal = curFD * 10 + curSD
            if (curVal > curMax):
                curMax = curVal

    return curMax

def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    peakJoltage = 0
    for d in data:
        peakJoltage += findPeakJolt(d)

    print(f"Part 1: {peakJoltage}")

if __name__ == "__main__":
    main(sys.argv)
