#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")


def addPts(pt0: tuple[int, int], pt1: tuple[int, int]) -> tuple[int,int]:
	retVal = ( pt0[0] + pt1[0], pt0[1] + pt1[1] )
	return retVal


class Grid:
	def __init__(self, inputData: list[str]):
		self.height = len(inputData)
		self.width = len(inputData[0])

		self.gridData = dict()
		for y, rowData in enumerate(inputData):
			for x, cellVal in enumerate(rowData):
				self.gridData[ (x,y) ] = cellVal

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

	def calculateNumWalls(self, region):
		

	def part2Cost(self):
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



def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	g = Grid(data)

	print(f"Part 1 = {g.part1Cost()}")


if __name__ == "__main__":
	main(sys.argv)
