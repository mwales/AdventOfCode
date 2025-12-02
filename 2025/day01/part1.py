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
        curRot = int(singleLine[1:])
        if singleLine[0] == "L":
            curVal = (curVal - curRot) % 100
        else:
            curVal = (curVal + curRot) % 100

        if curVal == 0:
            numZeros += 1
        debug(f"After {singleLine}, cur val = {curVal}")

    print(f"Part 1 = {numZeros}")

if __name__ == "__main__":
    main(sys.argv)
