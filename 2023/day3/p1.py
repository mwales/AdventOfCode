#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg + "\n")

def isSym(data, x, y):
	val = data[y][x]
	if (val == '.'):
		return False
	if ( (val >= '0') and (val <= '9') ):
		return False

	return True

def isInRange(data, x, y):
	if (x < 0):
		return False
	if (y < 0):
		return False
	if (x >= len(data[0])):
		return False
	if (y >= len(data)):
		return False
	return True

def isNextToSym(data, x, y, partNumLen):
	# check above
	xCBegin = x - 1
	xCEnd = x + 1 +partNumLen
	yC = y -1
	for xC in range(xCBegin, xCEnd):
		if isInRange(data, xC, yC):
			if isSym(data, xC, yC):
				return True

	# check left
	xC = x -1
	yC = y
	if isInRange(data, xC, yC):
		if isSym(data, xC, yC):
			return True


	# check right
	xC = x + partNumLen
	yC = y
	if isInRange(data, xC, yC):
		if isSym(data, xC, yC):
			return True


	# check under
	xCBegin = x - 1
	xCEnd = x + 1 + partNumLen
	yC = y + 1
	for xC in range(xCBegin, xCEnd):
		if isInRange(data, xC, yC):
			if isSym(data, xC, yC):
				return True

	debug(f"No syms near sym at {x},{y}")
	return False

def isPartNumber(data, x, y):
	partNum = ""
	while(x < len(data[0])):
		nextDigit = data[y][x]
		if ( (nextDigit >= '0') and (nextDigit <= '9') ):
			partNum += nextDigit
			x += 1
		else:
			break

	if (len(partNum) == 0):
		return None
	else:
		return int(partNum)

def getText(data, x, y):
	return data[y][x]

def printSchematic(data, goodParts):
	GOOD_COLOR = "ESC[38;5;{28}m"
	GOOD_COLOR = "\u001b[32m"
	BAD_COLOR = "ESC[38;5;{88}m"
	BAD_COLOR = "\u001b[31m"
	CLEAR_COLOR = "ESC[0m"
	CLEAR_COLOR = "\u001b[0m"

	goodCoordList = {}
	for pn in goodParts:
		goodCoordList[goodParts[pn]] = pn

	for y in range(len(data)):
		x = 0
		while (x < len(data[0])):
			coord = (x,y)
			if (coord in goodCoordList):
				sys.stdout.write(GOOD_COLOR)
				sys.stdout.write(str(goodCoordList[coord]))
				sys.stdout.write(CLEAR_COLOR)
				x += len(str(goodCoordList[coord]))
			else:
				val = getText(data, x, y)
				if ( (val >= '0') and (val <= '9') ):
					sys.stdout.write(BAD_COLOR)
					sys.stdout.write(val)
					sys.stdout.write(CLEAR_COLOR)
				else:
					sys.stdout.write(val)
				x += 1
		
		sys.stdout.write("\n")


	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	partNumList = {}
	for y in range(len(data)):
		x = 0
		while (x < len(data[0])):
			pn = isPartNumber(data, x, y)
			if (pn != None):
				partNumList[pn] = (x,y)
				x += len(str(pn))
			else:
				x += 1

	debug(f"List: {partNumList}")

	symGoodSum = 0
	goodParts = {}
	for pn in partNumList:
		coord = partNumList[pn]
		if (isNextToSym(data, coord[0], coord[1], len(str(pn)))):
			symGoodSum += pn
			goodParts[pn] =  coord
	
	print(symGoodSum)

	printSchematic(data, goodParts)


if __name__ == "__main__":
	main(sys.argv)
