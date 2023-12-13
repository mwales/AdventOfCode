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

	def checkVerticalMirrorLine(self, xMirror):
		debug(f"Checking for vertical mirror at {xMirror}")
		leftCols = xMirror
		rightCols = self.width - xMirror
		colsToMirror = min(leftCols, rightCols)
		
		errorCount = 0
		for xDelta in range(colsToMirror):
			for y in range(self.height):
				leftP = (xMirror - xDelta - 1, y)
				rightP = (xMirror + xDelta, y)
				if (self.getPoint(leftP) != self.getPoint(rightP)):
					errorCount += 1
					if errorCount >= 2:
						return False

		if errorCount == 0:
			# For part 2, need atleast 1 smudge
			return False

		return True

	def findVerticalMirrorLine(self):
		for xMirror in range(1, self.width):
			if self.checkVerticalMirrorLine(xMirror):
				return xMirror
		return -1

	def checkHorizontalMirrorLine(self, yMirror):
		debug(f"Checking for horizontal mirror at {yMirror}")
		topRows = yMirror
		bottomRows = self.height - yMirror
		rowsToMirror = min(topRows, bottomRows)
		
		errorCount = 0
		for yDelta in range(rowsToMirror):
			for x in range(self.width):
				topP = (x, yMirror - yDelta - 1)
				bottomP = (x, yMirror + yDelta)
				if (self.getPoint(topP) != self.getPoint(bottomP)):
					errorCount += 1
					if (errorCount >= 2):
						return False

		if (errorCount == 0):
			# Need atleast 1 smudge
			return False

		return True

	def findHorizontalMirrorLine(self):
		for yMirror in range(1, self.height):
			if self.checkHorizontalMirrorLine(yMirror):
				return yMirror
		return -1

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

	pList = []
	startRow = 0
	stopRow = 1
	while (startRow < len(data)):
		# Find the stop row
		while ( (stopRow < len(data)) and (data[stopRow] != "") ):
			stopRow += 1

		p = Pattern(data[startRow:stopRow])
		pList.append(p)

		startRow = stopRow + 1
		stopRow = startRow + 1

	debug("Done reading in data")

	p1Sum = 0
	for p in pList:
		mvl = p.findVerticalMirrorLine()
		debug(f"mvl = {mvl}")
		mhl = p.findHorizontalMirrorLine()
		debug(f"mhl = {mhl}")

		if (mvl == -1) and (mhl == -1):
			debug(f"This problem has no symmetry")
			print(p)
			return

		if (mvl != -1) and (mhl != -1):
			debug(f"This problem has duel symmetry")
			print(p)
			return

		if (mvl != -1):
			p1Sum += mvl
		if (mhl != -1):
			p1Sum += mhl * 100

	print(f"p1Sum = {p1Sum}")

if __name__ == "__main__":
	main(sys.argv)
