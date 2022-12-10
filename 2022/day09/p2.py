#!/usr/bin/env python3

import sys
import time

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def addPoint(x, y):
	retVal = (x[0] + y[0], x[1] + y[1])
	return retVal

def subPoint(x, y):
	retVal = (x[0] - y[0], x[1] - y[1])
	return retVal


class RopeTrail:
	def __init__(self, data, length):
		self.data = data

		self.ropePos = []
		for i in range(length):
			self.ropePos.append( (0, 0) )
		
		# Map bounds
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

		self.ropePos[0] = addPoint(self.ropePos[0], moveMap[direction])
		self.updateMapLimits(self.ropePos[0])

		for i in range(len(self.ropePos) - 1):
			self.followPoint(i)

		self.tailCrumbs.add(self.ropePos[-1])

	def followPoint(self, leaderNode):

		leaderPos = self.ropePos[leaderNode]
		followerPos = self.ropePos[leaderNode + 1]

		tailDist = subPoint(leaderPos, followerPos)
		eprint(tailDist)

		if (tailDist[0] <= -3) or (tailDist[0] >= 3) or (tailDist[1] <= -3) or (tailDist[1] >= 3):
			eprint("Leader node = {}".format(leaderNode))

			for i in range(len(self.ropePos)):
				eprint("node {} at {}".format(i, self.ropePos[i]))
			self.printMap()
			sys.exit(1)
		
		if (abs(tailDist[0]) >= 2) or (abs(tailDist[1]) >= 2):
			# Move diagnal
			if tailDist[0] == 0:
				movX = 0
			else:
				movX = tailDist[0] // abs(tailDist[0])

			if tailDist[1] == 0:
				movY = 0
			else:
				movY = tailDist[1] // abs(tailDist[1])
			followerPos = addPoint(followerPos, (movX, movY))

		self.ropePos[leaderNode + 1] = followerPos
		

	def propogateAllMoves(self):
		for line in self.data:
			#time.sleep(.1)
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
				else:
					for i in range(len(self.ropePos) - 1, -1, -1):
						if (curX, curY) == (self.ropePos[i]):
							curPixel = str(i)
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

	rt = RopeTrail(data, 10)
	
	rt.printBreadCrumbs()

	# My wrong answer is 2356
	print("Length of tail crumbs = {}".format(len(rt.tailCrumbs)))

if __name__ == "__main__":
	main(sys.argv)
