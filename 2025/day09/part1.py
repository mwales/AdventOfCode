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

    def area(self, otherPoint):
        area = abs(self.x - otherPoint.x) + 1
        area *= abs(self.y - otherPoint.y) + 1
        #debug(area)
        return area

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



    def countNeighbors(self, pt, searchVal):
        n_list = []
        n_list.append( Point(-1,-1) )
        n_list.append( Point(-1,0) )
        n_list.append( Point(-1,1) )
        n_list.append( Point(0,-1) )
        n_list.append( Point(0,1) )
        n_list.append( Point(1,-1) )
        n_list.append( Point(1,0) )
        n_list.append( Point(1,1) )

        n_count = 0
        for otherPoint in n_list:
            otherPoint.add(pt)
            if self.getVal(otherPoint) == searchVal:
                n_count += 1

        return n_count



def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    pointList = []
    for singleLine in data:
        p = tuple([ int(x) for x in singleLine.split(",") ])
        pointList.append(p)

    debug(pointList)

    bigArea = 1
    for i in range(len(pointList)):
        for j in range(len(pointList)):
            if i == j:
                continue
            p1 = Point(*pointList[i])
            p2 = Point(*pointList[j])
            bigArea = max( bigArea, p1.area(p2) )

    print(bigArea)



if __name__ == "__main__":
    main(sys.argv)
