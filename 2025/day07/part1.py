#!/usr/bin/env python3

import sys


def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, otherPoint):
        self.x += otherPoint.x
        self.y += otherPoint.y

class Grid:
    def __init__(self, input_lines):
        self.width = len(input_lines[0])
        self.height = len(input_lines)

        self.grid = dict()
        for y in range(self.height):
            for x in range(self.width):
                self.grid[ (x,y) ] = input_lines[y][x]

    def getVal(self, pt):
        if pt.x < 0 or pt.x >= self.width:
            return None

        if pt.y < 0 or pt.y >= self.height:
            return None

        return self.grid[ (pt.x, pt.y) ]

    def setVal(self, pt, val):
        if pt.x < 0 or pt.x >= self.width:
            return

        if pt.y < 0 or pt.y >= self.height:
            return

        self.grid[ (pt.x, pt.y) ] = val

    def printGrid(self):
        for y in range(self.height):
            curRow = ""
            for x in range(self.width):
                curRow += self.getVal( Point(x,y) )
            debug(curRow)

    def doBeam(self):
        for x in range(self.width):
            if self.getVal( Point(x,0) ) == "S":
                startOfBeam = x
                break

        currentBeams = set()
        currentBeams.add(startOfBeam)

        beamLevel = 0

        splitCount = 0
        for y in range(self.height):
            debug(f"\n\nNEW LEVEL, split count = {splitCount}")
            self.printGrid()
            splitBeams = set()

            nextStageBeams = currentBeams.copy()

            for cb in currentBeams:
                if self.getVal( Point(cb, y) ) == "^":
                    # hit a splitter
                    splitBeams.add(cb)
                    nextStageBeams.remove(cb)
                    splitCount += 1
                else:
                    # Tacyon in free space, add it to grid
                    self.setVal( Point(cb, y), '|')

            # Did any of the split tacyons create new beams?
            for nb in splitBeams:
                split = False
                if self.getVal( Point(nb + 1, y) ) != "|":
                    split = True
                    nextStageBeams.add(nb + 1)
                    self.setVal( Point(nb + 1, y), "|")
                    debug(f"Split at {nb + 1}")
                if self.getVal( Point(nb - 1, y) ) != "|":
                    split = True
                    nextStageBeams.add(nb - 1)
                    self.setVal( Point(nb - 1, y), "|")
                    debug(f"Split at {nb - 1}")


            currentBeams = nextStageBeams

        print(f"Splits = {splitCount}")


def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    g = Grid(data)

    g.doBeam()



if __name__ == "__main__":
    main(sys.argv)
