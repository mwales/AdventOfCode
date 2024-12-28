#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")


def addPts(pt0: tuple[int, int], pt1: tuple[int, int]) -> tuple[int,int]:
	retVal = ( pt0[0] + pt1[0], pt0[1] + pt1[1] )
	return retVal

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

		# Points are the same
		debug(f"Not a segment, points the same: {pt1} and {pt2}")

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

	def isNextToOtherSeg(self, otherSeg: Segment) -> Segment:
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

		# Overlapping
		print(f"How did we get here?")
		return None


class Grid:
	def __init__(self, inputData: list[str]):
		self.height = len(inputData)
		self.width = len(inputData[0])

		self.gridData = dict()
		for y, rowData in enumerate(inputData):
			for x, cellVal in enumerate(rowData):
				self.gridData[ (x,y) ] = cellVal

		self.dirList = [ (0,-1), (-1,0), (0,1), (1,0) ]

	def isInGrid(self, pt: tuple[int,int] ) -> bool:
		x = pt[0]
		y = pt[1]
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
				if (self.gridData[ (x,y) ] == region):
					retVal += 1
		return retVal

	def getAllPerim(self, region) -> int:
		retVal = 0
		neighbors = [ (-1,0), (0,-1), (1,0), (0,1) ]

		for x in range(self.width):
			for y in range(self.height):
				if (self.gridData[ (x,y) ] == region):
					for curDir in neighbors:
						nPt = addPts(curDir, (x,y) )
						if not self.isInGrid(nPt):
							retVal += 1
						elif self.gridData[nPt] != region:
							retVal += 1

		return retVal

	def getRegionPerim(self, region: list[ tuple[int,int]]) -> int:
		retVal = 0
		neighbors = [ (-1,0), (0,-1), (1,0), (0,1) ]

		for curPt in region:
			for direction in neighbors:
				neighPt = addPts( curPt, direction)

				if neighPt not in region:
					retVal += 1

		return retVal


	def floodRegion(self, pt: tuple[int,int]) -> list[ tuple[int,int] ]:
		retVal = []
		visitList = [pt]
		historyList = []
		curVal = self.gridData[pt]
		neighbors = [ (-1,0), (0,-1), (1,0), (0,1) ]
		while (len(visitList) > 0):
			curPt = visitList.pop(0)
			historyList.append(curPt)

			if (self.gridData[curPt] != curVal):
				continue

			retVal.append(curPt)

			for direction in neighbors:
				neighPt = addPts(curPt, direction)
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
				fullList.append( (x,y) )

		while(len(fullList) > 0):
			curPt = fullList[0]

			curReg = self.floodRegion(curPt)
			print(f"For region: {curReg}")
			curRegArea = len(curReg)
			curRegPerim = self.getRegionPerim(curReg)
			curRegCost = curRegArea * curRegPerim
			
			print(f"Random {self.gridData[curPt]} has {curRegArea} x {curRegPerim} = {curRegCost}")
			retVal += curRegCost

			# Remove all the region points from list
			for singlePt in curReg:
				print(f"  Remove {singlePt}")
				fullList.remove(singlePt)

		return retVal

	def getTurnRightDir(self, dirIndex) -> tuple[int, int]:
		dirIndex -= 1
		if (dirIndex < 0):
			dirIndex += 4
		return self.dirList[dirIndex]

	def getCurrentDir(self, dirIndex) -> tuple[int, int]:
		return self.dirList[dirIndex]
		
	def getTurnLeftDir(self, dirIndex) -> tuple[int, int]:
		dirIndex += 1
		dirIndex %= 4
		return self.dirList[dirIndex]
	
	def getBackwardsDir(self, dirIndex) -> tuple[int, int]:
		dirIndex += 2
		dirIndex %= 4
		return self.dirList[dirIndex]


	def calculateNumWallsWrong(self, region: list[ tuple[int, int]]):
		debug(f"calculateNumWalls of region {region}")

		# Find one of the low point in the region (and the left-most)
		startPt = region[0]
		for curPt in region:
			if (curPt[1] < startPt[1]):
				startPt = curPt
			if ( (curPt[1] == startPt[1]) and (curPt[0] < startPt[0]) ):
				startPt = curPt



		# Going to do directions as person dragging their right-hand against wall of maze

		wallVisitList = set()
		directionChanges = 0
		# Setting this purposely to wrong direction so we get a direction change right off the bat
		dirIndex = 1
		exitSearch = False
		curPt = startPt
		while(exitSearch == False):
			if (curPt in wallVisitList):
				# We are back to start point
				exitSearch = True
				continue

			wallVisitList.add(curPt)

			# Can I turn right?
			turnRtPt = addPts(curPt, self.getTurnRightDir(dirIndex))
			if (turnRtPt in region):
				# We can turn right, so we need to
				directionChanges += 1
				dirIndex -= 1
				if (dirIndex < 0):
					dirIndex += 4
				curPt = turnRtPt
				continue

			# Can I continue in same direction?
			sameDirPt = addPts(curPt, self.getCurrentDir(dirIndex))
			if (sameDirPt in region):
				# We can continue in the same direction
				curPt = sameDirPt
				continue

			#No?  How about left
			turnLeftPt = addPts(curPt, self.getTurnLeftDir(dirIndex))
			if (turnLeftPt in region):
				directionChanges += 1
				dirIndex += 1
				dirIndex %= 4
				curPt = turnLeftPt
				continue

			# How about turn 180
			deadEndPt = addPts(curPt, self.getBackwardsDir(dirIndex))
			if (deadEndPt in region):
				directionChanges += 2
				dirIndex += 2
				dirIndex %= 4
				curPt = deadEndPt
				continue

			# If we get here, I think this is the special case of a 1 square region?
			if (len(region) == 1):
				return 4

			# What the heck, how did we get here, this is all fail
			return None

		return directionChanges

	def createWallSegments(self, region: list[tuple[int,int]]) -> list[tuple[tuple[int,int], tuple[int,int]]]:
		# value of region
		if len(region) <= 0:
			return []

		# value of elements in region
		elemVal = self.gridData[ region[0] ]

		retList = []
		for curPt in region:
			curX, curY = curPt
			# 4 possible segments we need to generate (top, bottom, left, right)
			
			# check top
			if (curY == 0) or (self.gridData[ (curX, curY-1) ] != elemVal):
				ptA = curPt
				ptB = (curX + 1, curY)
				retList.append( (ptA,ptB) )

			# check bottom
			if (curY + 1 >= self.height) or (self.gridData[ (curX, curY+1) ] != elemVal):
				ptA = (curX, curY + 1)
				ptB = (curX + 1, curY + 1)
				retList.append( (ptA,ptB) )

			# check left
			if (curX == 0) or (self.gridData[ (curX-1,curY) ] != elemVal):
				ptA = (curX, curY)
				ptB = (curX, curY + 1)
				retList.append( (ptA,ptB) )

			# check right
			if (curX+1 >= self.width) or (self.gridData[ (curX+1,curY) ] != elemVal):
				ptA = (curX+1, curY)
				ptB = (curX+1, curY + 1)
				retList.append( (ptA,ptB) )


		debug(f"For region of {elemVal}, we have seg list:")
		for seg in retList:
			print(f"  Seg: {seg}")
		return retList

	def canWeJoinHorizontalSegs(self, seg1: tuple[int,int], seg2: tuple[int,int]) -> tuple[int,int]:
		# Are the segs horizontal?
		seg1x, seg1y = seg1
		seg2x, seg2y = seg2

		if (seg


	def canWeJoinVerticalSegs(self, seg1: tuple[tuple[int,int], seg2: tuple[int,int]) -> tuple[int,int]:


	def canWeJoin(self, firstSeg: tuple[int,int], otherSeg: tuple[int,int]) -> tuple[int,int]:
		# Return None if we can't, else the combined segment

		ptA, ptB = firstSeg
		ptAx, ptAy = ptA
		ptBx, ptBy = ptB

		# Is it a horizontal seg?
		if (ptAy == ptBy):
			# We always assume this is left seg, try to find seg to it's right
			for otherSeg in workingList:
				otherA, otherB = otherSeg
				otherAx, otherAy = otherA
				otherBx, otherBy = otherB

				# Matching seg must be horizontal
				if (otherAy == otherBy) and (otherAy == ptAy) and (ptBx == otherAx):
					combinedSeg = (ptA, otherB)
					retList.append(combinedSeg)
				workingList.remove(otherSeg)
					segCombined = True
					break

		else:
			# This must be a vertical seg
			# We always assume this is top seg, try to find seg underneath
			for otherSeg in workingList:
				otherA, otherB = otherSeg
				otherAx, otherAy = otherA
				otherBx, otherBy = otherB

				# Matching seg must be verticall too
				if (otherAx == otherBx) and (otherAx == ptAx) and (ptBy == otherAy):
					combinedSeg = (ptA, otherB)
					retList.append(combinedSeg)
					workingList.remove(otherSeg)
					segCombined = True
					break




	def joinSegs(self, segList: list[tuple[tuple[int,int], tuple[int,int]]] ) -> list[tuple[tuple[int,int], tuple[int,int]]]:
		retList = []
		workingList = segList[:]

		while len(workingList) >= 1:
			segCombined = False
			firstSeg = workingList.pop(0)

			# If that was the last seg, just add and quit
			if (len(workingList) == 0):
				retList.append(firstSeg)
				break

			ptA, ptB = firstSeg
			ptAx, ptAy = ptA
			ptBx, ptBy = ptB

			# Is it a horizontal seg?
			if (ptAy == ptBy):
				# We always assume this is left seg, try to find seg to it's right
				for otherSeg in workingList:
					otherA, otherB = otherSeg
					otherAx, otherAy = otherA
					otherBx, otherBy = otherB

					# Matching seg must be horizontal
					if (otherAy == otherBy) and (otherAy == ptAy) and (ptBx == otherAx):
						combinedSeg = (ptA, otherB)
						retList.append(combinedSeg)
						workingList.remove(otherSeg)
						segCombined = True
						break

			else:
				# This must be a vertical seg
				# We always assume this is top seg, try to find seg underneath
				for otherSeg in workingList:
					otherA, otherB = otherSeg
					otherAx, otherAy = otherA
					otherBx, otherBy = otherB

					# Matching seg must be verticall too
					if (otherAx == otherBx) and (otherAx == ptAx) and (ptBy == otherAy):
						combinedSeg = (ptA, otherB)
						retList.append(combinedSeg)
						workingList.remove(otherSeg)
						segCombined = True
						break

			# Did we combine the seg?
			if not segCombined:
				retList.append(firstSeg)

		return retList



						


	def calculateNumWalls(self, region: list[ tuple[int, int]]):
		segList = self.createWallSegments(region)

		oldLen = 0
		newLen = len(segList)
		while(oldLen != newLen):
			oldLen = len(segList)
			
			print("Combine some")
			segList = self.joinSegs(segList)


			debug(f"after combine, we have seg list:")
			for seg in segList:
				print(f"  Seg: {seg}")

			newLen = len(segList)


		return len(segList)

	def part2Cost(self):
		debug("Entering part 2")
		retVal = 0
		fullList = []
		for x in range(self.width):
			for y in range(self.height):
				fullList.append( (x,y) )

		while(len(fullList) > 0):
			curPt = fullList[0]

			curReg = self.floodRegion(curPt)
			print(f"For region: {curReg}")
			curRegArea = len(curReg)
			curRegNumWalls = self.calculateNumWalls(curReg)
			debug(f" curRegArea x curRegNumWalls = {curRegArea} x {curRegNumWalls}")
			curRegCost = curRegArea * curRegNumWalls
			
			print(f"Random {self.gridData[curPt]} has {curRegArea} x {curRegNumWalls} = {curRegCost}")
			retVal += curRegCost

			# Remove all the region points from list
			for singlePt in curReg:
				print(f"  Remove {singlePt}")
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
