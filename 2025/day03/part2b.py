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

def findMegaJolt(valStr, digitsLeft):
    debug(f"findMegaJolt({valStr},{digitsLeft})")

    topStrLen = len(valStr) - (digitsLeft - 1)
    topStr = valStr[:topStrLen]

    print(topStr)

    curFd = 0
    for curD in topStr:
        val = int(curD)
        if val > curFd:
            curFd = val

    debug(f"FD = {curFd}")

    if (digitsLeft == 1):
        return curFd

    firstPosOfFd = valStr.find(str(curFd))

    restOfStr = valStr[firstPosOfFd+1:]
    restOfMax = findMegaJolt(restOfStr, digitsLeft - 1)

    

    return int( str(curFd) + str(restOfMax) )



def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    peakJoltage = 0
    for d in data:
        tc = findMegaJolt(d, 12)
        debug(f"For line {d}, val = {tc}")
        peakJoltage += tc

    print(f"Part 2: {peakJoltage}")

if __name__ == "__main__":
    main(sys.argv)
