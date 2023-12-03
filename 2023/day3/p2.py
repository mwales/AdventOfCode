#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg + "\n")

def isSym(data, x, y):
	val = data[y][x]
	if (val == '.'):
		debug(f"  {x}, {y} not sym {val}")
		return False
	if ( (val >= '0') and (val <= '9') ):
		debug(f"  {x}, {y} not sym {val}")
		return False


	debug(f"  {x}, {y} IS sym {val}")
	return True

def isInRange(data, x, y):
	if (x < 0):
		debug(f"  {x}, {y} not in range")
		return False
	if (y < 0):
		debug(f"  {x}, {y} not in range")
		return False
	if (x >= len(data[0])):
		debug(f"  {x}, {y} not in range")
		return False
	if (y >= len(data)):
		debug(f"  {x}, {y} not in range")
		return False

	return True

def isNextToSym(data, x, y, partNumLen, pn):
	
	debug(f"Checking {pn} at {x},{y} for validity")

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

def getPossibleGears(data):
	asterixList = []
	for y in range(len(data)):
		for x in range(len(data[0])):
			tval = getText(data, x, y)
			if (tval == '*'):
				asterixList.append( (x,y) )

	return asterixList

def isAdjacentPartNum(data, xPart, yPart, xTest, yTest):
	xBeg = xPart - 1
	pn = getPartNumber(data, xPart, yPart)
	xEnd = xPart + len(pn) 
	yBeg = yPart - 1
	yEnd = yPart + 1

	if ( xBeg <= xTest <= xEnd):
		if (yBeg <= yTest <= yEnd):
			return True
	
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

def getPartNumber(data, x, y):
	pn = ""
	while(x < len(data[0])):
		val = data[y][x]
		if ( (val >= '0') and (val <= '9') ):
			pn += val
			x += 1
		else:
			break

	return pn

def printSchematic(data, goodParts):
	GOOD_COLOR = "ESC[38;5;{28}m"
	GOOD_COLOR = "\u001b[32m"
	BAD_COLOR = "ESC[38;5;{88}m"
	BAD_COLOR = "\u001b[31m"
	CLEAR_COLOR = "ESC[0m"
	CLEAR_COLOR = "\u001b[0m"

	for y in range(len(data)):
		x = 0
		while (x < len(data[0])):
			coord = (x,y)
			if (coord in goodParts):
				sys.stdout.write(GOOD_COLOR)
				pn = getPartNumber(data, x, y)
				sys.stdout.write(pn)
				sys.stdout.write(CLEAR_COLOR)
				x += len(pn)
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

	partCoordList = []
	for y in range(len(data)):
		x = 0
		while (x < len(data[0])):
			pn = isPartNumber(data, x, y)
			if (pn != None):
				partCoordList.append( (x,y) )
				x += len(str(pn))
			else:
				x += 1

	debug(f"List: {partCoordList}")

	gearList = getPossibleGears(data)
	debug(f"Poss Gear List = {gearList}")

	possibleGearParts = set()
	for coord in partCoordList:
		for possGear in gearList:
			if isAdjacentPartNum(data, *coord, *possGear):
				possibleGearParts.add(coord)
			
	#printSchematic(data, goodParts)
	debug(f"Set of poss gears now = {possibleGearParts}")

	gearRatio = 0
	progress = 0
	debug(f"Number of poss gears {len(gearList)}")

	for possGearPos in gearList:
		progress += 1
		debug(f"Progress update: {progress} with ratio {gearRatio}")

		grAdd = 0
		for firstPart in possibleGearParts:
			for secondPart in possibleGearParts:
				if (firstPart == secondPart):
					continue

				if (isAdjacentPartNum(data, *firstPart, *possGearPos) and
				    isAdjacentPartNum(data, *secondPart, *possGearPos) ):
					grAdd = int(getPartNumber(data, *firstPart)) * int(getPartNumber(data, *secondPart))
		gearRatio += grAdd
			
	print(gearRatio)

if __name__ == "__main__":
	main(sys.argv)
