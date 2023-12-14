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
		debug("Not implemented")

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



def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	p = Pattern(data)
	p.tiltDirection(0,-1)

	debug(p)

	l = p.analyzeLoad()
	print(l)


if __name__ == "__main__":
	main(sys.argv)
