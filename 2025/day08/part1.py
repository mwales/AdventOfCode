#!/usr/bin/env python3

import sys
import math

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

class Point3d:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

    def from3Ints(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def add(self, otherPoint):
        self.x += otherPoint.x
        self.y += otherPoint.y
        self.z += otherPoint.z

    def dist(self, otherPoint):
        deltaX = self.x - otherPoint.x
        deltaY = self.y - otherPoint.y
        deltaZ = self.z - otherPoint.z
        retval = (deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ) ** 0.5
        return retval

    def toTuple(self):
        return (self.x, self.y, self.z)

    def fromTuple(self, t):
        (self.x, self.y, self.z) = t

class CircuitList:
    def __init__(self):
        self.circuitList = []

    def addJunction(self, p1, p2):
        p1_in_circ = None
        p2_in_circ = None

        for cIndex in range(len(self.circuitList)):
            if p1 in self.circuitList[cIndex]:
                p1_in_circ = cIndex

            if p2 in self.circuitList[cIndex]:
                p2_in_circ = cIndex

        # Neither are in a circuit
        if p1_in_circ == None and p2_in_circ == None:
            # Make their own circuit
            new_circ = []
            new_circ.append(p1)
            new_circ.append(p2)
            self.circuitList.append(new_circ)
            debug("  New circuit")
            return

        # If they are already on the same circuit
        if p1_in_circ == p2_in_circ:
            # do nothing, they are already connected
            debug("  Already connected in same circuit")
            return

        # 1 is connected, and one isn't, join existing circuit
        if p1_in_circ == None and p2_in_circ != None:
            self.circuitList[p2_in_circ].append(p1)
            debug("  Joining existing circuit")
            return

        if p1_in_circ != None and p2_in_circ == None:
            self.circuitList[p1_in_circ].append(p2)
            debug("  Joining existing circuit")
            return

        # if you got here, the are in different circuits, need to merge them
        debug("  Merging 2 circuits")
        for otherPoints in self.circuitList[p2_in_circ]:
            self.circuitList[p1_in_circ].append(otherPoints)

        self.circuitList.pop(p2_in_circ)

    def print(self):
        for i in range(len(self.circuitList)):
            debug(f"{i}: {self.circuitList[i]}")

    def numJunctionsConnected(self):
        ret_val = 0
        for c in self.circuitList:
            ret_val += len(c)
        return ret_val

    def getCircuitLens(self):
        ret_val = []
        for c in self.circuitList:
            ret_val.append(len(c))
        return ret_val


class PointList:
    def __init__(self):
        self.pointList = []
            
    def addPointsFromStrings(self, data):
        for single_line in data:
            pointParts = single_line.split(",")
            point3d = tuple( [ int(x) for x in pointParts ] )
            debug(point3d)
            self.pointList.append(point3d)

    def calcAllLength(self):

        ret_val = []
        for i in range(len(self.pointList)):
            for j in range(len(self.pointList)):
                if i == j:
                    continue

                pi = Point3d()
                pi.fromTuple(self.pointList[i])
                pj = Point3d()
                pj.fromTuple(self.pointList[j])

                d = pi.dist(pj)

                ret_val.append( (d, pi.toTuple(), pj.toTuple() ) )

        ret_val.sort()
        return ret_val

def main(argv):

    if (len(argv) < 3):
        print("Usage: {} inputfile numJunctionsToJoin".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    num_juncs_to_join = int(argv[2])

    main_pl = PointList()
    main_pl.addPointsFromStrings(data)

    cl = CircuitList()

    # This list ends up with each set segment twice:  p1,p2 and p2,p1
    closestPoints = main_pl.calcAllLength()

    debug("Print closest points list:")
    for cp in closestPoints:
        debug(cp)

    for i in range(0, num_juncs_to_join * 2, 2):

        #if cl.numJunctionsConnected() >= num_juncs_to_join:
        #    break

        (dist, p1, p2) = closestPoints[i]
        debug(f"Adding {p1} and {p2}")
        cl.addJunction(p1,p2)

        cl.print()

    len_list = cl.getCircuitLens()
    len_list.sort()

    len_list.reverse()
    
    print(f"List Len = {len_list}")

    part1 = 1
    for i in range(3):
        debug(f"Length {i} = {len_list[i]}")
        part1 *= len_list[i]

    print(part1)

if __name__ == "__main__":
    main(sys.argv)
