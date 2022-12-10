#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def addPoint(x, y):
	retVal = (x[0] + y[0], x[1] + y[1])
	return retVal

def subPoint(x, y):
	retVal = (x[0] - y[0], x[1] - y[1])
	return retVal


class RopeTrail:
	def __init__(self, data):
		self.data = data

		self.headPos = (0, 0)
		self.tailPos = (0, 0)
		self.mapXLow = -2
		self.mapXHigh = 2
		self.mapYLow = -2
		self.mapYHigh = 2
		self.tailCrumbs = set()

		self.propogateAllMoves()

		self.printBreadCrumbs()

		self.printMap()

	def moveHeadTo(self, direction):
		eprint("Move Head to {}".format(direction))
		moveMap = { 'U': (0, -1), 'D': (0,1), 'L':(-1,0), 'R':(1,0) }

		self.headPos = addPoint(self.headPos, moveMap[direction])
		self.updateMapLimits(self.headPos)

		tailDist = subPoint(self.headPos, self.tailPos)
		eprint(tailDist)
		
		if (tailDist[0] <= -2):
			self.tailPos = (self.headPos[0] + 1, self.headPos[1])
		if (tailDist[0] >= 2):
			self.tailPos = (self.headPos[0] - 1, self.headPos[1])

		if (tailDist[1] <= -2):
			self.tailPos = (self.headPos[0], self.headPos[1] + 1)
		if (tailDist[1] >= 2):
			self.tailPos = (self.headPos[0], self.headPos[1] - 1)

		self.tailCrumbs.add(self.tailPos)
		

	def propogateAllMoves(self):
		for line in self.data:
			eprint("== {} ==".format(line))
			lineParts = line.split(" ")
			for i in range(int(lineParts[1])):
				self.moveHeadTo(lineParts[0])
				self.printMap()

	def printBreadCrumbs(self):
		eprint("Bread Crumbs:")
		for curY in range(self.mapYLow, self.mapYHigh+1):
			curRow = ""
			for curX in range(self.mapXLow, self.mapXHigh + 1):
				curPixel = '.'
				if (curX, curY) in (0,0):
					curPixel = 's'
				elif (curX, curY) in self.tailCrumbs:
					curPixel = '#'
				curRow += curPixel
			eprint(curRow)



	def printMap(self):

		eprint("Map!")
		for curY in range(self.mapYLow, self.mapYHigh+1):
			curRow = ""
			for curX in range(self.mapXLow, self.mapXHigh + 1):
				curPixel = '.'
				if (curX, curY) == (0,0):
					curPixel = 's'
				elif (curX, curY) in self.tailCrumbs:
					curPixel = '#'
				elif (curX, curY) == (self.tailPos):
					curPixel = 'T'
				elif (curX, curY) == (self.headPos):
					curPixel = 'H'
				curRow += curPixel
			eprint(curRow)

	def updateMapLimits(self, dataPoint):
		if self.mapXLow > dataPoint[0]:
			self.mapXLow = dataPoint[0]
		if self.mapXHigh < dataPoint[0]:
			self.mapXHigh = dataPoint[0]

		if self.mapYLow > dataPoint[1]:
			self.mapYLow = dataPoint[1]
		if self.mapYHigh < dataPoint[1]:
			self.mapYHigh = dataPoint[1]






def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	rt = RopeTrail(data)
	
	rt.printBreadCrumbs()

	print("Length of tail crumbs = {}".format(len(rt.tailCrumbs)))

if __name__ == "__main__":
	main(sys.argv)
