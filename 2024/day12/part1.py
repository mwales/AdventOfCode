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

	def joinSeg(self, otherSeg: Segment) -> Segment:
		if (self.isHorizontal() != otherSeg.isHorizontal()):
			return None

		if (self.isVertical() != otherSeg.isVertical()):
			return None

		# if it's the same seg, not next to
		if (self.equal(otherSeg)):
			return None

		if (self.isVertical()):
			# Same X?
			if self.pt1.x != otherSeg.pt1.x:
				return None

			# Do we have a shared Y?
			if (self.pt2.y == otherSeg.pt1.y):
				retVal = Segment(self.pt1, otherSeg.pt2)
				return retVal
			elif (otherSeg.pt2.y == self.pt1.y):
				retVal = Segment(self.pt2, otherSeg.pt1)
				return retVal
			else:
				return None

		if (self.isHorizontal()):
			# Same Y?
			if (self.pt1.y != otherSeg.pt1.y):
				return None

			# Do we have a shared X?
			if (self.pt2.x == otherSeg.pt1.x):
				retVal = Segment(self.pt1, otherSeg.pt2)
				return retVal
			elif (otherSeg.pt2.x == self.pt1.x):
				retVal = Segment(self.pt2, otherSeg.pt1)
				return retVal
			else:
				return None

		# Overlapping
		debug(f"How did we get here join segs? {self} and {otherSeg}")
		return None


class Grid:
	def __init__(self, inputData: list[str]):
		self.height = len(inputData)
		self.width = len(inputData[0])

		self.gridData = dict()
		for y, rowData in enumerate(inputData):
			for x, cellVal in enumerate(rowData):
				curPoint = Point(x,y)
				self.gridData[ curPoint ] = cellVal

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

	def getAllArea(self, region) -> int:
		retVal = 0
		for x in range(self.width):
			for y in range(self.height):
				if (self.gridData[ Point(x,y) ] == region):
					retVal += 1
		return retVal

	def getRegionPerim(self, region: list[ Point ]) -> int:
		retVal = 0

		for curPt in region:
			for direction in self.dirList:
				neighPt = curPt.add(direction)

				if neighPt not in region:
					retVal += 1

		return retVal


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

	def part1Cost(self):
		retVal = 0
		fullList = []
		for x in range(self.width):
			for y in range(self.height):
				fullList.append( Point(x,y) )

		while(len(fullList) > 0):
			curPt = fullList[0]

			curReg = self.floodRegion(curPt)
			debug(f"For region: {curReg}")
			curRegArea = len(curReg)
			curRegPerim = self.getRegionPerim(curReg)
			curRegCost = curRegArea * curRegPerim
			
			debug(f"Random {self.gridData[curPt]} has {curRegArea} x {curRegPerim} = {curRegCost}")
			retVal += curRegCost

			# Remove all the region points from list
			for singlePt in curReg:
				debug(f"  Remove {singlePt}")
				fullList.remove(singlePt)

		return retVal
	
	def createWallSegments(self, region: list[Point]) -> list[Segment]:
		# value of region
		if len(region) <= 0:
			return []

		# value of elements in region
		elemVal = self.gridData[ region[0] ]

		retList = []
		for curPt in region:
			curX = curPt.x
			curY = curPt.y
			# 4 possible segments we need to generate (top, bottom, left, right)
			
			# check top
			if (curY == 0) or (self.gridData[ Point(curX, curY-1) ] != elemVal):
				ptA = curPt
				ptB = Point(curX + 1, curY)
				retList.append( Segment(ptA,ptB) )

			# check bottom
			if (curY + 1 >= self.height) or (self.gridData[ Point(curX, curY+1) ] != elemVal):
				ptA = Point(curX, curY + 1)
				ptB = Point(curX + 1, curY + 1)
				retList.append( Segment(ptA,ptB) )

			# check left
			if (curX == 0) or (self.gridData[ Point(curX-1,curY) ] != elemVal):
				ptA = Point(curX, curY)
				ptB = Point(curX, curY + 1)
				retList.append( Segment(ptA,ptB) )

			# check right
			if (curX+1 >= self.width) or (self.gridData[ Point(curX+1,curY) ] != elemVal):
				ptA = Point(curX+1, curY)
				ptB = Point(curX+1, curY + 1)
				retList.append( Segment(ptA,ptB) )


		debug(f"For region of {elemVal}, we have seg list:")
		for seg in retList:
			debug(f"  Seg: {seg}")
		return retList

	def isSegOnGridBorder(self, s: Segment) -> bool:
		if (s.isVertical()):
			if (s.pt1.x == 0):
				# is it on left edge
				return True
			elif (s.pt1.x == self.width):
				# is it on right edge
				return True
			else:
				# on neither edge
				return False
		elif (s.isHorizontal()):
			if (s.pt1.y == 0):
				# is on top edge
				return True
			elif (s.pt1.y == self.height):
				return True
			else:
				return False
		else:
			# borders are only horizontal or vertical
			return False

	def isLongerSegValid(self, newSeg: Segment, val : str) -> bool:
		segLen = newSeg.length()
		if (newSeg.isVertical()):
			# is our val on the left or right side?
			curPt = newSeg.pt1.add(Point(-1,0))
			deltaPt = Point(0,1)
			if self.gridData[curPt] == val:
				# We are going to check the left side of vertical
				debug(f"isLongerSegValid {newSeg} for {val} checking left side")
			else:
				curPt = curPt.add( Point(1,0) )
				debug(f"isLongerSegValid {newSeg} for {val} checking right side")

		elif (newSeg.isHorizontal()):
			curPt = newSeg.pt1.add(Point(0,-1))
			deltaPt = Point(1,0)
			if (self.gridData[curPt] == val):
				# We are goiong to check the top side of horizontal
				debug(f"isLongerSegValid {newSeg} for {val} checking top side")
			else:
				curPt = curPt.add(Point(0,1))
				debug(f"isLongerSegValid {newSeg} for {val} checking bottom side")

		else:
			debug(f"Failed validation, not horizontal or vertical {newSeg}")
			return False

		for i in range(segLen):
			if self.gridData[curPt] != val:
				return False

			curPt = curPt.add(deltaPt)


		return True

	def joinSegs(self, segList: list[Segment], val: str ) -> list[Segment]:
		retList = []
		workingList = segList[:]

		while len(workingList) >= 1:
			segCombined = False
			firstSeg = workingList.pop(0)

			# If that was the last seg, just add and quit
			if (len(workingList) == 0):
				retList.append(firstSeg)
				break

			for otherSeg in workingList:
				resultSeg = firstSeg.joinSeg(otherSeg)

				if (resultSeg == None):
					debug(f"  Not able to join segs: {firstSeg} and {otherSeg}")
					# These segs aren't close enough to join
					continue

				debug(f"  Attempt to join segs: {firstSeg} and {otherSeg} into {resultSeg}")

				# The segs are close enough to join, is the resultant seg valid?
				# Disallow touching corners!
				if (self.isSegOnGridBorder(resultSeg)):
					# Segs on the border are valid
					debug(f"    New seg {resultSeg} is on border, is valid")
					retList.append(resultSeg)
					workingList.remove(otherSeg)
					segCombined = True
					break
				elif (self.isLongerSegValid(resultSeg, val)):
					debug(f"    New seg {resultSeg} passed validation")
					retList.append(resultSeg)
					workingList.remove(otherSeg)
					segCombined = True
					break

				if (self.isLongerSegValid(resultSeg, val)):
					retList.append(resultSeg)
					workingList.remove(otherSeg)
					segCombined = True
					break

			if (segCombined == False):
				retList.append(firstSeg)

		return retList


	def calculateNumWalls(self, region: list[ Point ]):
		segList = self.createWallSegments(region)
		regVal = self.gridData[region[0]]

		oldLen = 0
		newLen = len(segList)
		while(oldLen != newLen):
			oldLen = len(segList)
			
			debug("Combine some")
			segList = self.joinSegs(segList, regVal)


			debug(f"after combine, we have seg list:")
			for seg in segList:
				debug(f"  Seg: {seg}")

			newLen = len(segList)


		return len(segList)

	def part2Cost(self):
		debug("Entering part 2")
		retVal = 0
		fullList = []
		for x in range(self.width):
			for y in range(self.height):
				fullList.append( Point(x,y) )

		while(len(fullList) > 0):
			curPt = fullList[0]

			curReg = self.floodRegion(curPt)
			debug(f"For region: {curReg}")
			curRegArea = len(curReg)
			curRegNumWalls = self.calculateNumWalls(curReg)
			debug(f" curRegArea x curRegNumWalls = {curRegArea} x {curRegNumWalls}")
			curRegCost = curRegArea * curRegNumWalls
			
			debug(f"Random {self.gridData[curPt]} has {curRegArea} x {curRegNumWalls} = {curRegCost}")
			retVal += curRegCost

			# Remove all the region points from list
			for singlePt in curReg:
				debug(f"  Remove {singlePt}")
				fullList.remove(singlePt)

		return retVal


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	g = Grid(data)

	print(f"Part 1 = {g.part1Cost()}")

	p2 = g.part2Cost()
	print(f"Part 2 = {p2}")

if __name__ == "__main__":
	main(sys.argv)
