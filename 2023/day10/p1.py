#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

class PipeMap:
	def __init__(self, td):
		self.width = len(td[0])
		self.height = len(td)

		self.td = td

	def getSym(self, x, y):
		return self.td[y][x]

	def isCoordValid(self, x, y):
		if (x < 0) or (y < 0):
			return False
		if (x >= self.width) or (y >= self.height):
			return False
		return True
	
	def getStartPos(self):
		for x in range(self.width):
			for y in range(self.height):
				if (self.getSym(x,y) == 'S'):
					return (x,y)
		
		debug("Failed to find the start of the map")
		return None

	def getAllNeighbors(self, x, y):
		possibleN = [ (x+1, y), (x-1, y), (x, y+1), (x, y-1) ]
		goodN = []
		for p in possibleN:
			if ( self.isCoordValid( *p ) ):
				goodN.append(p)

		return goodN

	def getAllStartNeighbors(self):
		sp = self.getStartPos()
		debug(f"StartPos= {sp}")
		allSn = self.getAllNeighbors(*sp)
		retVal = []
		for singleN in allSn:
			connectedList = self.getConnectedLocs(*singleN)
			if sp in connectedList:
				retVal.append(singleN)

		return retVal

	def getConnectedLocs(self, x, y):
		curSym = self.getSym(x,y)
		connectionMap = { '|': [ (x,y+1), (x, y-1) ],
		                  '-': [ (x+1, y), (x-1, y) ],
		                  'L': [ (x+1, y), (x, y-1) ],
		                  'J': [ (x-1, y), (x, y-1) ],
		                  'F': [ (x+1, y), (x, y+1) ],
		                  '7': [ (x-1, y), (x, y+1) ],
						  'S': [],
						  '.': [] }

		retVal = []
		for pl in connectionMap[curSym]:
			if self.isCoordValid( *pl ):
				retVal.append(pl)
		debug(f"From point {x},{y} you can reach: {retVal}")
		return retVal

	def getPipeDest(self, x, y, curPos):
		destinations = self.getConnectedLocs(x,y)
		if (destinations[0] == curPos):
			retVal = destinations[1]
		else:
			retVal = destinations[0]
		debug(f"getPipeDest(pipe@{x},{y}, with curPos={curPos} returned dest {retVal}")
		return retVal

	def solveMap(self):
		startPos = self.getStartPos()
		startNeighbors = self.getAllStartNeighbors()
		if (len(startNeighbors) != 2):
			print(f"Abort: startN = {startNeighbors}")
			return

		breadcrumbs = [ set(), set() ]
		breadcrumbs[0].add(startPos)
		breadcrumbs[1].add(startPos)
		curPos = startNeighbors[:]
		oldPos = [ startPos, startPos ]
		stepCount = 1
		debug(f"Start of solve from {curPos}")
		while(curPos[0] != curPos[1]):
			for i in range(len(curPos)):
				curX = curPos[i][0]
				curY = curPos[i][1]
				pd = self.getPipeDest(curX, curY, oldPos[i])
				oldPos[i] = curPos[i]
				curPos[i] = pd
				debug(f"For step {stepCount}, side {i} moved to {curPos[i]}")
			stepCount += 1
	
		return stepCount

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	pm = PipeMap(data)
	sol = pm.solveMap()
	print(sol)



if __name__ == "__main__":
	main(sys.argv)
