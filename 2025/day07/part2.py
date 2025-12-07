#!/usr/bin/env python3

import sys
import copy

def debug(msg):
    if False:
        sys.stderr.write(f"{msg}\n")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, otherPoint):
        self.x += otherPoint.x
        self.y += otherPoint.y

    def __str__(self):
        return f"({self.x},{self.y})"

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
    
    def doBeam(self, startPoint):
        debug(f"doBeam({startPoint}")

        beamLevel = 0
        num_timelines = 0

        for y in range(startPoint.y, self.height):
            debug(f"\n\nNEW LEVEL")
            self.printGrid()
            splitBeams = set()

            cb = startPoint.x

            if self.getVal( Point(cb, y) ) == "^":
                # hit a splitter

                left_timeline = copy.deepcopy(self)
                num_timelines += left_timeline.doBeam( Point(cb - 1, y+1) )
                right_timeline = copy.deepcopy(self)
                num_timelines += right_timeline.doBeam( Point(cb + 1, y+1) )
                return num_timelines
            else:
                # Tacyon in free space, add it to grid
                self.setVal( Point(cb, y), '|')


        return 1


def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    g = Grid(data)

    for x in range(g.width):
        if g.getVal( Point(x,0) ) == "S":
            startOfBeam = x
            break


    nt = g.doBeam( Point(x,0) )
    print(f"NT = {nt}")



if __name__ == "__main__":
    main(sys.argv)
