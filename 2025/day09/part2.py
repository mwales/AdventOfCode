#!/usr/bin/env python3

'''
I abandoned this non-working solution.  Didn't like the solution for determining
which squares were valid areas, and wasn't sure if it would actually work
'''

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

    def toTuple(self):
        return (self.x,self.y)

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

class LineList:
    def __init__(self, polarity):
        self.ll = []
        self.pointList = []
        self.polarity = polarity
        self.directionList=[]

    def determineDirection(self, p1, p2):
        deltaX = p2.x - p1.x
        deltaY = p2.y - p1.y

        if deltaX > 0:
            direction= "R"
        elif deltaX < 0:
            direction = "L"
        elif deltaY > 0:
            direction = "D"
        else:
            direction = "U"

        return direction
    
    def fillDirection(self, oldDirection, newDirection, oldFillDir):
        if oldDirection == newDirection:
            # Haven't changed directions
            return oldFillDir

        # Check for opp directions
        if ( oldDirection == "U" and newDirection == "D" ) or \
           ( oldDirection == "D" and newDirection == "U" ):
            print("Opposite direction path")
        
        if ( oldDirection == "L" and newDirection == "R" ) or \
           ( oldDirection == "R" and newDirection == "L" ):
            print("Opposite direction path")

        if oldDirection == "U":
            if newDirection == "L":
                newFd = "U" if oldFillDir == "R" else "D"
            if newDirection == "R":
                newFd = "U" if oldFillDir == "L" else "D"
        elif oldDirection == "D":    
            if newDirection == "L":
                newFd = "U" if oldFillDir == "L" else "D"
            if newDirection == "R":
                newFd = "U" if oldFillDir == "R" else "D"

        elif oldDirection == "R":    
            if newDirection == "U":
                newFd = "L" if oldFillDir == "U" else "R"
            if newDirection == "D":
                newFd = "L" if oldFillDir == "D" else "R"
        elif oldDirection == "L":    
            if newDirection == "U":
                newFd = "L" if oldFillDir == "D" else "R"
            if newDirection == "D":
                newFd = "L" if oldFillDir == "U" else "R"





    def addLines(self, data):
        # determine start direction
        for singleLine in data:
            p = tuple([ int(x) for x in singleLine.split(",") ])
            self.pointList.append(p)

        for i in range(len(self.pointList)):
            
            # line direction
            p1 = Point(*self.pointList[i])
            p2 = Point(*self.pointList[(i + 1) % len(self.pointList)])
            direction = self.determineDirection(p1, p2)

            self.ll.append( (direction, p1.toTuple(), p2.toTuple()) )

    def getProspectiveRectangles(self):
        rectList = []
        for i in range(len(self.pointList)):
            for j in range(len(self.pointList)):

                if (i == j):
                    continue

                p1 = Point(*self.pointList[i])
                p2 = Point(*self.pointList[j])

                area = p1.area(p2)

                t1 = (area, p1.toTuple(), p2.toTuple())
                t2 = (area, p2.toTuple(), p1.toTuple())

                if t1 in rectList or t2 in rectList:
                    continue

                rectList.append(t1)

        rectList.sort()
        rectList.reverse()
        return rectList

    def filterRectsWithPointsInside(self, rectList):
        filteredList = []
        for cur_rect in rectList:
            p1 = Point(*cur_rect[1])
            p2 = Point(*cur_rect[2])

            minX = min(p1.x, p2.x)
            maxX = max(p1.x, p2.x)

            minY = min(p1.y, p2.y)
            maxY = max(p1.y, p2.y)

            deltaX = maxX - minX
            deltaY = maxY - minY

            if deltaX < 2 or deltaY < 2:
                # box is too small ot have any points inside of it
                filteredList.append(cur_rect)
                continue

            minX += 1
            maxX -= 1
            minY += 1
            maxY -= 1

            foundPointInZone = False
            for otherPoint in self.pointList:
                op = Point(*otherPoint)
                if minY < op.x < maxX and minY < op.y < maxY:
                    foundPointInZone = True

            if foundPointInZone:
                continue

            filteredList.append(cur_rect)

        return filteredList
                
    def filterRectsWithPolarity(self, rectList):            
        filteredList = []
        for cur_rect in rectList:
            p1 = Point(*cur_rect[1])
            p2 = Point(*cur_rect[2])

                      



        


def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    ll = LineList(True)
    ll.addLines(data)

    pr = ll.getProspectiveRectangles()

    debug("All candidates")
    debug(pr)

    debug("All candidates with no points in zone")
    pr = ll.filterRectsWithPointsInside(pr)

    debug(pr)
if __name__ == "__main__":
    main(sys.argv)
