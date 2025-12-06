#!/usr/bin/env python3

import sys


def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

def isFresh(db, ingred):
    for fdata in db:
        if fdata[0] <= ingred <= fdata[1]:
            return True
    return False


def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    dbReadMode = True
    db = []
    num_fresh = 0
    for line in data:
        if line == "":
            debug("End of DB entries")
            dbReadMode = False
            continue

        debug(line)

        if dbReadMode:
            fRange = line.split("-")
            fStart = int(fRange[0])
            fEnd = int(fRange[1])
            db.append( (fStart, fEnd) )
        else:
            if isFresh(db, int(line)):
                num_fresh += 1

    print(f"fresh = {num_fresh}")

if __name__ == "__main__":
    main(sys.argv)
