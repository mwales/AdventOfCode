#!/usr/bin/env python3

import sys


def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")
'''
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
'''
def doMath(values, operation):
    ret_val = values[0]
    for i in range(1, len(values)):
        if operation == "+":
            ret_val += values[i]
        else:
            operation *= values[i]
    return ret_val

def replace_char(orig_str, pos, new_char):
    ret_str = orig_str[:pos] + new_char + orig_str[pos+1:]
    return ret_str

def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    seperator_cols = []
    x = 0
    y = 0
    while( x < len(data[0])):
        while(True):
            if data[y][x] != ' ':
                y = 0
                x += 1
                break
            
            y += 1
            if y == len(data):
                seperator_cols.append(x)
                x += 1
                y = 0
                break

    debug(f"cols = {seperator_cols}")

    for x in range(len(data[0])):
        for y in range(len(data)):
            if x in seperator_cols:
                data[y] = replace_char(data[y], x, ",")

    
    rows = []
    operations = data[-1].split(",")
    for y in range(len(data) - 1):
        rows.append( [ int(x) for x in data[y].split(",") ] )

    solution = 0

    for x in range(len(rows[0])):
        colVal = rows[0][x]
        for cur_row in range(1, len(rows)):
            if operations[x].strip() == "+":
                colVal += rows[cur_row][x]
            elif operations[x].strip() == "*":
                colVal *= rows[cur_row][x]

        solution += colVal

    print(f"Solution: {solution}")



if __name__ == "__main__":
    main(sys.argv)
