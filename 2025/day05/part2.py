#!/usr/bin/env python3

import sys


def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

class NumberLine:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop 

    def doesOtherUnionTouch(self, otherUnion):
        if otherUnion.stop < self.start:
            return False
        if otherUnion.start > self.stop:
            return False

        return True

    def mergeWithOtherUnion(self, otherUnion):
        self.start = min(self.start, otherUnion.start)
        self.stop = max(self.stop, otherUnion.stop)

    def size(self):
        return self.stop - self.start + 1

    def print(self):
        debug(f"  {self.start} - {self.stop}")

class FreshDB:

    def printList(self):
        for nl in self.db:
            nl.print()

    def __init__(self):
        self.db = []

    def add_range(self, start, stop):
        if len(self.db) == 0:
            self.db.append( NumberLine(start, stop) )

        curNL = NumberLine(start,stop)

        for otherNL in self.db:
            if otherNL.doesOtherUnionTouch(curNL):
                otherNL.mergeWithOtherUnion(curNL)
                return

        self.db.append(curNL)
        
    def count_freshies(self):

        num_fresh = 0

        for curNL in self.db:
            num_fresh += curNL.size()

        return num_fresh

    def optimize(self):
        for i in range(len(self.db)):
            for j in range(len(self.db)):
                if i == j:
                    continue

                if self.db[i].doesOtherUnionTouch(self.db[j]):
                    debug("Ewww, the following are TOUCHING each other")
                    self.db[i].print()
                    self.db[j].print()

                    self.db[i].mergeWithOtherUnion(self.db[j])

                    self.db.pop(j)
                    return True
        debug(f"Found nothing touching during optimization")
        return False

def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    dbReadMode = True
    db = FreshDB()
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
            db.add_range(fStart,fEnd)
            db.printList()         

    db.printList()

    while(db.optimize()):
        debug("Optimizing")

    nf = db.count_freshies()
    print(f"Part 2 = {nf}")


if __name__ == "__main__":
    main(sys.argv)
