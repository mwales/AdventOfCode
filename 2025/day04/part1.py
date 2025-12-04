#!/usr/bin/env python3

import sys

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
            return '.'

        if pt.y < 0 or pt.y >= self.height:
            return '.'

        return self.grid[ (pt.x, pt.y) ]

    def countNeighbors(self, pt):
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
            if self.getVal(otherPoint) == '@':
                n_count += 1

        return n_count




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

    g = Grid(data)

    part1_count = 0
    for x in range(g.width):
        for y in range(g.height):
            
            curPoint = Point(x,y)
            if g.getVal(curPoint) == '@' and g.countNeighbors(curPoint) < 4:
                part1_count += 1


    print(f"Solve: {part1_count}")
                



if __name__ == "__main__":
    main(sys.argv)
