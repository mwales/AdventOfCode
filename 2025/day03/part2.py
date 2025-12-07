#!/usr/bin/env python3

# This solution is slow as molasses, so while it ran I found better solve
#
# /usr/bin/time ./part2.py input.txt
# 318536.92user 26.01system 88:30:34elapsed 99%CPU (0avgtext+0avgdata 9588maxresident)k      
# 0inputs+0outputs (0major+1115minor)pagefaults 0swaps
#
# And it even got the correct answer!


import sys

def debug(msg):
    if False:
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
    curMax = 0
    debug(f"findMegaJolt({valStr},{digitsLeft})")
    if digitsLeft == len(valStr):
        debug(f"Special case, len == digits left, returning {valStr}")
        return int(valStr)

    if digitsLeft == 1:
        for curLetter in valStr:
            v = int(curLetter)
            if v > curMax:
                curMax = v
        debug(f"Special case, len == 1, return {curMax}")
        return curMax

    nextCallDigitsLeft = digitsLeft - 1
    maxFd = 0
    for i in range(len(valStr) - digitsLeft + 1):
        curFd = int(valStr[i])
        debug(f"Testing curFd = {curFd}, rest = {valStr[i+1:]}, maxFd = {maxFd}")
        if (curFd < maxFd):
            continue

        maxFd = curFd
        curVal = curFd * (10 ** nextCallDigitsLeft)
        curVal += findMegaJolt(valStr[i+1:], nextCallDigitsLeft)

        if (curVal > curMax):
            curMax = curVal

    debug(f"findMegaJolt({valStr},{digitsLeft}) returning {curMax}")
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
        tc = findMegaJolt(d, 12)
        print(f"For line {d}, val = {tc}")
        peakJoltage += tc

    print(f"Part 2: {peakJoltage}")

if __name__ == "__main__":
    main(sys.argv)
