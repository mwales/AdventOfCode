#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def numInListLessThan(listData, number):
	retVal = 0
	for curItem in listData:
		if curItem < number:
			retVal += 1
	
	debug(f"numInListLessThan({listData},{number}) returning {retVal}")
	return retVal

class Galaxy:
	def __init__(self, name):
		self.name = name

	def initGalaxyData(self, data):
		self.rawData = data
		self.width = len(data[0])
		self.height = len(data)

		self.galaxies = [ ]

		self.galaxyCount = 0
		for y in range(self.height):
			for x in range(self.width):
				curChar = self.rawPoint(x,y)
				if (curChar == '#'):
					self.galaxies.append( (x,y) )

	def initGalaxySize(self, width, height):
		self.width = width
		self.height = height
		self.galaxies = []
		self.galaxyCount = 0

	def rawPoint(self, x, y):
		return self.rawData[y][x]

	def printGalaxy(self):
		debug(f"Solar System: {self.name}")
		for y in range(self.height):
			curRow = ""
			for x in range(self.width):
				if (x,y) in self.galaxies:
					curRow += "#"
				else:
					curRow += "."
			debug(curRow)

	def isRowEmpty(self, y):
		for x in range(self.width):
			if (x,y) in self.galaxies:
				return False
		return True
	
	def isColEmpty(self, x):
		for y in range(self.height):
			if (x,y) in self.galaxies:
				return False
		return True
		
	
	def createExpandedGalaxy(self):
		listOfColsToExpand = []
		listOfRowsToExpand = []

		for y in range(self.height):
			if (self.isRowEmpty(y)):
				listOfRowsToExpand.append(y)

		for x in range(self.width):
			if (self.isColEmpty(x)):
				listOfColsToExpand.append(x)

		debug(f"Cols to expand: {listOfColsToExpand}")
		debug(f"Rows to expand: {listOfRowsToExpand}")

		ng = Galaxy("expanded " + self.name)
		ng.initGalaxySize(self.width + len(listOfColsToExpand), self.height + len(listOfRowsToExpand))
		for p in self.galaxies:
			modX = p[0] + numInListLessThan(listOfColsToExpand, p[0])
			modY = p[1] + numInListLessThan(listOfRowsToExpand, p[1])
			ng.galaxies.append( (modX, modY) )

		return ng

	def createGalaxyPairList(self):
		megaList = set()
		for num1 in range(len(self.galaxies)):
			for num2 in range(len(self.galaxies)):
				if (num1 == num2):
					continue

				if num1 < num2:
					entry = (num1, num2)
				else:
					entry = (num2, num1)

				megaList.add(entry)
		debug(f"createGalaxyPairList ret: {megaList}")
		return megaList
	
	def computeDistance(self, galaxy1, galaxy2):
		g1 = self.galaxies[galaxy1]
		g2 = self.galaxies[galaxy2]
		deltaX = abs(g1[0] - g2[0])
		deltaY = abs(g1[1] - g2[1])
		return deltaX + deltaY

		
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	g = Galaxy("orig")
	g.initGalaxyData(data)

	g.printGalaxy()

	eg = g.createExpandedGalaxy()
	eg.printGalaxy()

	ml = eg.createGalaxyPairList()
	debug(f"Num pairings: {len(ml)}")

	totalDist = 0
	for curPair in ml:
		totalDist += eg.computeDistance( *curPair )
	print(totalDist)

if __name__ == "__main__":
	main(sys.argv)
