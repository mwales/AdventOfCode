#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def addPoints(pt1: tuple[int,int], pt2: tuple[int, int] ) -> tuple[int,int]:
	retVal = (pt1[0] + pt2[0], pt1[1] + pt2[1])
	debug(f" addPoints( {pt1}, {pt2}) = {retVal}")
	return retVal

def scalePoint(pt1: tuple[int, int], scalar: int) -> tuple[int,int]:
	retVal = ( pt1[0] * scalar, pt1[1] * scalar)
	#debug(f"scalePoint( {pt1}, {scalar}) = {retVal}")
	return retVal

def subPoints(pt1: tuple[int,int], pt2: tuple[int, int] ) -> tuple[int,int]:
	pt2minus = scalePoint(pt2, -1)
	retVal = addPoints(pt1, pt2minus)
	debug(f" subPoints( {pt1}, {pt2}) = {retVal}")
	return retVal

class SignalMap:
	def __init__(self, inputData: list[str]):
		self.height = len(inputData)
		self.width = len(inputData[0])

		self.mapEntries = dict()
		for y, rowData in enumerate(inputData):
			for x, cellVal in enumerate(rowData):
				if (cellVal != '.'):
					self.mapEntries[ (x,y) ] = cellVal

	def isInMap(self, pt: tuple[int, int] ) -> bool:
		x = pt[0]
		y = pt[1]
		if (x < 0) or (x >= self.width):
			debug(f"isInMap( {pt} ) = False (bad x)")
			return False

		if (y < 0) or (y >= self.height):
			debug(f"isInMap( {pt} ) = False (bad y)")
			return False
			
		debug(f"isInMap( {pt} ) = True")
		return True

	def findAntinodes(self) -> list[ tuple[int,int]]:
		antList = set()

		for item1 in self.mapEntries.keys():
			for item2 in self.mapEntries.keys():
				if (item1 == item2):
					continue

				cell1Val = self.mapEntries[item1]
				cell2Val = self.mapEntries[item2]

				if (cell1Val != cell2Val):
					continue

				debug(f"  2 pts: {item1} and {item2}")

				# These 2 points will have 2 antinodes
				diffVal = subPoints(item1, item2)

				stillOnMap = True
				anti1 = item1
				while(stillOnMap):
					anti1 = addPoints(anti1,diffVal)
					if (self.isInMap(anti1)):
						antList.add(anti1)
					else:
						stillOnMap = False

				anti2 = item1
				stillOnMap = True
				while(stillOnMap):
					anti2 = subPoints(anti2,diffVal)
					if (self.isInMap(anti2)):
						antList.add(anti2)
					else:
						stillOnMap = False
		
		debug(f"findAntinodes() = {antList}")
		return antList

	def printMap(self, printAntinodes: bool):
		if (printAntinodes):
			antList = self.findAntinodes()
	
		for y in range(self.height):
			curRowStr = ""
			for x in range(self.width):
				curPt = (x,y)
				curMapVal = "."
				if (curPt in self.mapEntries):
					curMapVal = self.mapEntries[curPt]

				if printAntinodes and (curPt in antList):
					curMapVal = '#'

				curRowStr += curMapVal
			print(curRowStr)




def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	sm = SignalMap(data)
	sm.printMap(True)

	part1 = sm.findAntinodes()
	print(f"part1 = {len(part1)}")


if __name__ == "__main__":
	main(sys.argv)
