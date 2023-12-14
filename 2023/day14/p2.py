#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		#sys.stderr.write(f"{msg}\n")
		print(msg)


class Pattern:
	def __init__(self, data):
		self.width = len(data[0])
		self.height = len(data)
		debug(f"New pattern that is {self.width} x {self.height}")
		self.data = data

	def isPointInRange(self, p):
		(x,y) = p
		if ( (x < 0) or (x >= self.width) ):
			return False

		if ( (y < 0) or (y >= self.height) ):
			return False
		return True

	def getPoint(self, p):
		(x,y) = p
		return self.data[y][x]
	
	def setPoint(self, p, val):
		(x,y) = p
		newRowData = self.data[y][:x] + val + self.data[y][x+1:]
		self.data[y] = newRowData

	def tiltVertical(self, yDir):
		if yDir == -1:
			startRow = 0
			endRow = self.height
		else:
			startRow = self.height - 1
			endRow = -1

		for x in range(self.width):
			tiltedFlag = True
			while(tiltedFlag):
				tiltedFlag = False
				emptySpot = -1
				y = startRow
				while(y != endRow):
					cp = (x,y)
					curObj = self.getPoint(cp)
					if ( (curObj == '.') and (emptySpot == -1) ):
						emptySpot = y
					if (curObj == '#'):
						emptySpot = -1
					if ( (curObj == 'O') and (emptySpot != -1) ):
						self.setPoint(cp, '.')
						self.setPoint((x,emptySpot), 'O')
						tiltedFlag = True
						break
					y -= yDir

						

	def tiltHorizontal(self, xDir):
		if xDir == -1:
			startCol = 0
			endCol = self.width
		else:
			startCol = self.width - 1
			endCol = -1

		for y in range(self.height):
			tiltedFlag = True
			while(tiltedFlag):
				tiltedFlag = False
				emptySpot = -1
				x = startCol
				while(x != endCol):
					cp = (x,y)
					curObj = self.getPoint(cp)
					if ( (curObj == '.') and (emptySpot == -1) ):
						emptySpot = x
					if (curObj == '#'):
						emptySpot = -1
					if ( (curObj == 'O') and (emptySpot != -1) ):
						self.setPoint(cp, '.')
						self.setPoint((emptySpot, y), 'O')
						tiltedFlag = True
						break
					x -= xDir


	def tiltDirection(self, xDir, yDir):
		# one of either xDir or yDir should be -1 or 1
		if (xDir == 0):
			self.tiltVertical(yDir)
		else:
			self.tiltHorizontal(xDir)

	def analyzeLoad(self):
		loadVal = 0
		for y in range(self.height):
			for x in range(self.width):
				curVal = self.getPoint( (x,y) )
				if (curVal == 'O'):
					loadVal += (self.height - y)
		return loadVal

	def __repr__(self):
		retData = f"** Pattern is {self.width} x {self.height}\n"
		for y in range(self.height):
			for x in range(self.width):
				retData += self.getPoint( (x,y) )
			retData += "\n"
		return retData

	def spinCycle(self):
		self.tiltDirection(0, -1)
		self.tiltDirection(-1,0)
		self.tiltDirection(0, 1)
		self.tiltDirection(1,0)

	def getCopy(self):
		retVal = Pattern(self.data[:])
		return retVal

	def comparePattern(self, other):
		for y in range(self.height):
			if (self.data[y] != other.data[y]):
				return False
		return True

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	p = Pattern(data)

	oldP = [ p.getCopy() ]

	i = 0
	endCycleCount = 1000000000
	while i < endCycleCount:
		i += 1
		p.spinCycle()
		debug(f"After {i}")
		#debug(p)

		for j in range(len(oldP)):
			if p.comparePattern(oldP[j]):
				# We found a repeating pattern.
				debug(f"Repeating of {j} at {i}")
				diff = i - j
				cyclesLeft = endCycleCount - i
				numRepeats = cyclesLeft // diff
				debug(f"Cycles left = {cyclesLeft} and numRepeatLoops = {numRepeats}")
				advance = numRepeats * diff
				debug(f"Advancing {advance} from {i} to {i+advance}")
				i += advance
				break

		oldP.append(p.getCopy())

	debug("Now non-opt version")
	
	while i < endCycleCount:
		i += 1
		p.spinCycle()
		debug(f"After {i}")
		#debug(p)

		oldP.append(p.getCopy())
		i += 1

	l = p.analyzeLoad()
	print(l)


if __name__ == "__main__":
	main(sys.argv)
