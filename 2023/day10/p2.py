#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
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

	def getStepDirection(self, oldPos, firstStep):
		deltaX = firstStep[0] - oldPos[0]
		deltaY = firstStep[1] - oldPos[1]
		if (deltaX == 1):
			return 'R'
		if (deltaX == -1):
			return 'L'
		if (deltaY == 1):
			return 'D'
		if (deltaY == -1):
			return 'U'

		debug(f"Failed to compute direction from {oldPos} and {firstStep}")
		return None

	def addFill(self, fillLeft, curPos, direction):
		x = curPos[0]
		y = curPos[1]
		fillLeftMap = { 'U': (x-1, y),
		                'D': (x+1, y),
		                'L': (x, y+1),
		                'R': (x, y-1) }
		fillRightMap = { 'U': (x+1, y),
		                 'D': (x-1, y),
		                 'L': (x, y-1),
		                 'R': (x, y+1) }

		if fillLeft:
			fillPos = [ fillLeftMap[direction] ]
		else:
			fillPos = [ fillRightMap[direction] ]

		curSym = self.getSym( *curPos )
		if ( (curSym == 'J') or (curSym == '7') or (curSym == 'L') or (curSym == 'F') ):
			if (curSym == 'J'):
				if (direction == 'R') and (fillLeft == False):
					fillPos.append( (x+1,y) )
				if (direction == 'D') and (fillLeft == True):
					fillPos.append( (x,y+1) )

			if (curSym == '7'):
				if (direction == 'L') and (fillLeft == True):
					fillPos.append( (x+1,y) )
				if (direction == 'U') and (fillLeft == False):
					fillPos.append( (x, y-1) )

			if (curSym == 'L'):
				if (direction == 'D') and (fillLeft == False):
					fillPos.append( (x,y+1) )
				if (direction == 'L') and (fillLeft == True):
					fillPos.append( (x-1,y) )

			if (curSym == 'F'):
				if (direction == 'U') and (fillLeft == True):
					fillPos.append( (x,y-1) )
				if (direction == 'L') and (fillLeft == False):
					fillPos.append( (x-1,y) )

		return fillPos

	def getFullPipeMap(self, fillLeft):
		startPos = self.getStartPos()
		startNeighbors = self.getAllStartNeighbors()
		if (len(startNeighbors) != 2):
			print(f"Abort: startN = {startNeighbors}")
			return

		breadcrumbs = []
		floodList = []
		breadcrumbs.append(startPos)
		curPos = startNeighbors[0]
		oldPos = startPos
		debug(f"Start of solve from {curPos}")
		curDirection = self.getStepDirection(startPos, curPos)
		debug(f"Start direction = {curDirection}")
		while(True):
			breadcrumbs.append(curPos)

			curX = curPos[0]
			curY = curPos[1]
			pd = self.getPipeDest(curX, curY, oldPos)
			oldPos = curPos
			curPos = pd

			
			curDirection = self.getStepDirection(oldPos, curPos)
			fillPoint = self.addFill(fillLeft, curPos, curDirection)
			floodList.extend(fillPoint)
			debug(f"Direction changed to {curDirection} and filled {fillPoint}")
			debug(f"For step side moved to {curPos}")
			if (curPos == startPos):
				break

		floodRetVal = []
		for p in floodList:
			if p not in breadcrumbs:
				floodRetVal.append(p)

		debug(f"Final flood fill list = {floodRetVal}")

		return breadcrumbs, floodRetVal
	
	def printMapWithPipe(self):
		pipeLocs, floodLocs = self.getFullPipeMap(True)
		for y in range(self.height):
			mapRow = ""
			for x in range(self.width):
				if (x,y) in pipeLocs:
					mapRow += "*"
				else:
					mapRow += "."
			debug(mapRow)

	def finishFlood(self, pipeLoc, floodStarts):
		floodData = set()
		tryFlood = set()
		for p in floodStarts:
			floodData.add(p)
			tryFlood.add(p)

		while(len(tryFlood) > 0):
			curFloodPoint = tryFlood.pop()
			nextFloodPoints = self.getAllNeighbors(*curFloodPoint)
			for nfp in nextFloodPoints:
				if (nfp not in pipeLoc) and (nfp not in floodData):
					floodData.add(nfp)
					tryFlood.add(nfp)
					
		return floodData
				

	
	def printFloodMapWithPipe(self, floodLeft):
		pipeLocs, floodLocs = self.getFullPipeMap(floodLeft)

		finalFlood = self.finishFlood(pipeLocs, floodLocs)

		for y in range(self.height):
			mapRow = ""
			for x in range(self.width):
				if (x,y) in pipeLocs:
					mapRow += "*"
				elif (x,y) in finalFlood:
					mapRow += 'F'
				else:
					mapRow += "."
			print(mapRow)

		return finalFlood

		

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	pm = PipeMap(data)
	sol = pm.getFullPipeMap(True)
	print(sol)

	print("Flood Left")
	floodLeftList = pm.printFloodMapWithPipe(True)


	print()

	print("Flood Right")
	floodRightList = pm.printFloodMapWithPipe(False)

	print()

	print(f"FL = {len(floodLeftList)} and FR = {len(floodRightList)}")


if __name__ == "__main__":
	main(sys.argv)
