#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def addPoints(pt1: tuple[int,int], pt2: tuple[int, int] ) -> tuple[int,int]:
	retVal = (pt1[0] + pt2[0], pt1[1] + pt2[1])
	#debug(f" addPoints( {pt1}, {pt2}) = {retVal}")
	return retVal

def scalePoint(pt1: tuple[int, int], scalar: int) -> tuple[int,int]:
	retVal = ( pt1[0] * scalar, pt1[1] * scalar)
	#debug(f"scalePoint( {pt1}, {scalar}) = {retVal}")
	return retVal

def subPoints(pt1: tuple[int,int], pt2: tuple[int, int] ) -> tuple[int,int]:
	pt2minus = scalePoint(pt2, -1)
	retVal = addPoints(pt1, pt2minus)
	#debug(f" subPoints( {pt1}, {pt2}) = {retVal}")
	return retVal

class Grid:
	def __init__(self, inputData: list[str]):
		self.height = len(inputData)
		self.width = len(inputData[0])

		self.mapEntries = dict()
		for y, rowData in enumerate(inputData):
			for x, cellVal in enumerate(rowData):
				if (cellVal != '.'):
					self.mapEntries[ (x,y) ] = int(cellVal)

	def isInMap(self, pt: tuple[int, int] ) -> bool:
		x = pt[0]
		y = pt[1]
		if (x < 0) or (x >= self.width):
			#debug(f"isInMap( {pt} ) = False (bad x)")
			return False

		if (y < 0) or (y >= self.height):
			#debug(f"isInMap( {pt} ) = False (bad y)")
			return False
			
		#debug(f"isInMap( {pt} ) = True")
		return True

	def printMap(self):
	
		for y in range(self.height):
			curRowStr = ""
			for x in range(self.width):
				curPt = (x,y)
				curMapVal = "."
				if (curPt in self.mapEntries):
					curMapVal = self.mapEntries[curPt]


				curRowStr += str(curMapVal)
			print(curRowStr)

	def findTrailhead(self) -> list[ tuple[int,int] ]:
		retVal = []
		for x in range(self.width):
			for y in range(self.height):
				curPt = (x,y)
				if (self.mapEntries[curPt] == 0):
					retVal.append(curPt)

		return retVal

	def findTrailEndsFromPt(self, trailStart: tuple[int,int], startHeight: int) -> set[ tuple [int,int] ]:
		debug(f"findTrailEndsFromPt({trailStart},{startHeight})")
		nextHeight = startHeight + 1
		dirUpdateList = [ (0,1), (0,-1), (1,0), (-1,0) ]

		retVal = set()
		if (startHeight == 9):
			# this is winner
			retVal.add(trailStart)
			return retVal

		for curDir in dirUpdateList:
			nextPt = addPoints(trailStart, curDir)
			if not self.isInMap(nextPt):
				continue

			if self.mapEntries[nextPt] == nextHeight:
				retVal |= self.findTrailEndsFromPt(nextPt, nextHeight)
		
		return retVal




	def findTrailEnds(self) -> set[ tuple [int,int] ]:

		retVal = set()
		headList = self.findTrailhead()
		for head in headList:
			retVal |= self.findTrailEndsFromPt(head, 0)
		return retVal

	def part1(self) -> int:
		retVal = 0
		headList = self.findTrailhead()
		for head in headList:
			retVal += len(self.findTrailEndsFromPt(head, 0))
		return retVal



def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	g = Grid(data)
	g.printMap()

	part1Data = g.part1()
	print(part1Data)

if __name__ == "__main__":
	main(sys.argv)
