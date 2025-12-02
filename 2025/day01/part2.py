#!/usr/bin/env python3

import sys

def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")



def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    curVal = 50
    numZeros = 0
    for singleLine in data:
        #debug(f"Cur line = {singleLine}")
        curRot = int(singleLine[1:])
        oldVal = curVal
        if singleLine[0] == "L":
            curVal = (curVal - curRot) 
        else:
            curVal = (curVal + curRot)

        if (oldVal > 0) and (curVal < 0):
            numZeros +=1
            debug("Crossed zero pos to neg")
        elif (oldVal < 0) and (curVal > 0):
            numZeros += 1
            debug("Crossed zero neg to pos")

        if abs(curVal) > 100:
            numZeros += abs(curVal) // 100
            if (abs(curVal) // 100):
                debug(f"Rotated past 100 {abs(curVal) // 100} times")
        

        if (curVal % 100) == 0 and abs(curVal) > 100:
            debug("Landed right on zero (but already counted)")
            #numZeros += 1
            curVal %= 100
        else:
            curVal %= 100
            if (curVal == 0):
                numZeros += 1
                debug("Landed right on zero")
        debug(f"After {singleLine}, cur val = {curVal}, numZeros = {numZeros}")

    print(f"Part 1 = {numZeros}")

if __name__ == "__main__":
    main(sys.argv)
