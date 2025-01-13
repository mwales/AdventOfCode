#!/usr/bin/env python3

from __future__ import annotations
from typing import Any

import sys

def debug(msg):
	if False:
		sys.stderr.write(f"{msg}\n")

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def add(self, otherPt: Point) -> Point:
		retVal = Point(self.x + otherPt.x, self.y + otherPt.y)
		return retVal

	def scale(self, scalar:int):
		self.x *= scalar
		self.y *= scalar

	def minus(self, otherPt: Point) -> Point:
		otherInverted = Point(otherPt.x * -1, otherPt.y * -1)
		retVal = self.add(otherInverted)
		return retVal

	def __eq__(self, other: Any):
		if isinstance(other, Point):
			return self.x == other.x and self.y == other.y
		else:
			return False

	def __hash__(self):
		return hash( (self.x, self.y) )

	def __repr__(self):
		retVal = f"(x={self.x},y={self.y})"
		return retVal

class Segment:
	def __init__(self, pt1: Point, pt2: Point):
		# order the segments to make future work easier
		if (pt1.x < pt2.x):
			self.pt1 = pt1
			self.pt2 = pt2
		elif (pt1.x > pt2.x):
			self.pt1 = pt2
			self.pt2 = pt1

		else:
			if (pt1.y < pt2.y):
				self.pt1 = pt1
				self.pt2 = pt2
			elif (pt1.y > pt2.y):
				self.pt1 = pt2
				self.pt2 = pt1
			else:
				# Points are the same
				debug(f"Not a segment, points the same: {pt1} and {pt2}")

	def __repr__(self) -> str:
		retVal = f"[ ({self.pt1.x},{self.pt1.y}) - ({self.pt2.x},{self.pt2.y}) ]"
		return retVal

	def equal(self, otherSeg) -> bool:
		if (self.pt1 == otherSeg.pt1) and (self.pt2 == otherSeg.pt2):
			return True

		if (self.pt2 == otherSeg.pt1) and (self.pt1 == otherSeg.pt2):
			return True

		return False

	def isHorizontal(self) -> bool:
		if self.pt1.y == self.pt2.y:
			return True
		else:
			return False

	def isVertical(self) -> bool:
		if self.pt1.x == self.pt2.x:
			return True
		else:
			return False
	
	def length(self):
		if self.isHorizontal():
			return self.pt2.x - self.pt1.x
		elif self.isVertical():
			return self.pt2.y - self.pt1.y
		else:
			deltaX = self.pt2.x - self.pt1.x
			deltaY = self.pt2.y - self.pt1.y
			return pow(deltaX * deltaX + deltaY * deltaY)

class Robot:
	def __init__(self, data, width, height):
		parts = data.split(" ")
		if (len(parts) < 2):
			print(f"Error processing: {data}")
			return

		robotPosParts = parts[0].split(",")
		robotVelParts = parts[1].split(",")

		robotPosX = int(robotPosParts[0][2:])
		robotPosY = int(robotPosParts[1])
		
		robotVelX = int(robotVelParts[0][2:])
		robotVelY = int(robotVelParts[1])

		self.robotPos = Point(robotPosX, robotPosY)
		self.robotVel = Point(robotVelX, robotVelY)

		self.width = width
		self.height = height

	def iterateState(self, numIterations):
		debug(f"Commanded to iterated {numIterations}")
		debug(f"Current robot pos {self.robotPos} and vel {self.robotVel}")

		robotMoveDelta = self.robotVel
		robotMoveDelta.scale(numIterations)
		newRobotPos = self.robotPos.add(robotMoveDelta)
		
		inGridPos = Point(newRobotPos.x % self.width,
		                  newRobotPos.y % self.height)
		self.robotPos = inGridPos
		
		debug(f"New robot pos {self.robotPos} and vel {self.robotVel}")

	def __repr__(self) -> str:
		retVal = f"Robot [ pos={self.robotPos} vel={self.robotVel} ]"
		return retVal

	def __hash__(self):
		return hash( (self.robotPos, self.robotVel) )




class Grid:
	def __init__(self, inputData: list[str], width, height):
		self.height = height
		self.width = width

		self.gridData = dict()

		self.robotList = list()
		for line in inputData:
			r = Robot(line, width, height)
			self.robotList.append(r)
			debug(f"Added robot: {r}")

		self.dirList = [ Point(0,-1), Point(-1,0), Point(0,1), Point(1,0) ]

	def isInGrid(self, pt: Point ) -> bool:
		x = pt.x
		y = pt.y
		if (x < 0) or (x >= self.width):
			return False

		if (y < 0) or (y >= self.height):
			return False

		return True

	def getRegionList(self) -> list[str]:
		retVal = set()
		for x in range(self.width):
			for y in range(self.height):
				retVal.add(self.gridData[ (x,y) ])
		return list(retVal)

	def floodRegion(self, pt: Point) -> list[ Point ]:
		retVal = []
		visitList = [pt]
		historyList = []
		curVal = self.gridData[pt]
		while (len(visitList) > 0):
			curPt = visitList.pop(0)
			historyList.append(curPt)

			if (self.gridData[curPt] != curVal):
				continue

			retVal.append(curPt)

			for direction in self.dirList:
				neighPt = curPt.add(direction)
				if ( (self.isInGrid(neighPt)) and
				     (neighPt not in historyList) and 
				     (neighPt not in visitList) ):
					visitList.append(neighPt)
		
		return retVal

	def displayGrid(self):
		for y in range(self.height):
			rowText = ""
			for x in range(self.width):
				curPt = Point(x,y)
				numRobots = 0
				for r in self.robotList:
					if (r.robotPos == curPt):
						numRobots += 1

				if (numRobots > 9):
					rowText += "+"
				elif (numRobots == 0):
					rowText += "."
				else:
					rowText += str(numRobots)

			print(rowText)

	def iterateState(self, numIterations):
		for r in self.robotList:
			r.iterateState(numIterations)

	def calculateSafetyFactor(self):
		sfSums = [ 0,0,0,0 ]
		
		halfwidth = self.width // 2
		halfheight = self.height // 2

		for r in self.robotList:
			if (r.robotPos.x < halfwidth and r.robotPos.y < halfheight):
				sfSums[0] += 1
			elif (r.robotPos.x > halfwidth and r.robotPos.y < halfheight):
				sfSums[1] += 1
			elif (r.robotPos.x < halfwidth and r.robotPos.y > halfheight):
				sfSums[2] += 1
			elif (r.robotPos.x > halfwidth and r.robotPos.y > halfheight):
				sfSums[3] += 1


		debug(f"The quads = {sfSums}")
		multAll = 1
		for s in sfSums:
			multAll *= s

		return multAll





def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	g = Grid(data, 101, 103)

	g.displayGrid()
	
	debug(f"After 100 iterations");
	g.iterateState(100)
	g.displayGrid()

	sf = g.calculateSafetyFactor()
	print(sf)


if __name__ == "__main__":
	main(sys.argv)
