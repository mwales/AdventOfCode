#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def getNeighborPoints(x, y, mapData):
	retVal = set()
	# Check N
	if (y >= 1):
		retVal.add( (x,y-1) )
	
	# Check S
	if (y + 1 < len(mapData)):
		retVal.add( (x,y+1) )
	
	# Chech W
	if (x >= 1):
		retVal.add( (x-1, y) )
	
	# Check E
	if ( x + 1 < len(mapData[0])):
		retVal.add( (x+1,y) )
		
	return retVal
	
def getHeight(x, y, mapData):
	return int(mapData[y][x])
	
def isPointLow(x, y, mapData):
	# Get our point
	pt = getHeight(x,y,mapData)
	
	neighbors = getNeighborPoints(x, y, mapData)
	# eprint("Ns: {}".format(neighbors))
	for eachN in neighbors:
		(xCheck, yCheck) = eachN
		if (pt >= getHeight(xCheck, yCheck, mapData)):
			return False
	
	return True
	
# Starting from a low point, create a set of points for the basin by
# filling the basin up 1 level at a time
def fillBasin(x, y, mapData):
	retVal = set()
	retVal.add((x,y))
	curHeight = getHeight(x, y, mapData) + 1
	
	checkMe = getNeighborPoints(x, y, mapData)
	while (curHeight < 9):
		nextCheck = set()
		for eachPoint in checkMe:
			ptX, ptY = eachPoint
			if eachPoint in retVal:
				#eprint("{} already part of basin at {},{}".format(eachPoint, x, y))
				continue
			
			h = getHeight(ptX, ptY, mapData)
			if ( h == curHeight):
				#eprint("({} is part of basin at {},{}".format(eachPoint, x, y))
				retVal.add(eachPoint)
				for nn in getNeighborPoints(ptX, ptY, mapData):
					nextCheck.add(nn)
				continue
				
			if (h == 9):
				#eprint("{} is height 9, not part of a basin".format(eachPoint))
				continue
				
			if (h < curHeight):
				#eprint("{} is to low, cant be part of basin {},{}".format(eachPoint, x, y))
				continue
				
			# check again
			nextCheck.add(eachPoint)
		
		#eprint("Finished check for h = {}".format(curHeight))
		curHeight += 1
		checkMe = nextCheck
		
	return retVal

# Size of the top 3 basins multiplied together
def scoreBasins(basinList):
	sizeList = [ len(x) for x in basinList ]
	
	score = 1
	maxThree = []
	for i in range(3):
		maxSize = max(sizeList)
		score *= maxSize
		sizeList.remove(maxSize)
		maxThree.append(maxSize)
		
	scoreStrs = [ str(x) for x in maxThree ]
	eprint("Score = {} = {}".format(" * ".join(scoreStrs), score))
	return score

	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	w = len(filedata[0])
	h = len(filedata)
	
	lowPoints = set()
	for x in range(w):
		for y in range(h):
			if isPointLow(x, y, filedata):
				lowPoints.add( (x,y) )
				
	print("Low Points = {}".format(lowPoints))
	
	basinCollection = []
	for lp in lowPoints:
		x,y = lp
		eprint("Creating basin for {}".format(lp))
		basinPoints = fillBasin(x,y, filedata)
		print("Basin pts: {}".format(basinPoints))
		print("Basin size: {}".format(len(basinPoints)))
		basinCollection.append(basinPoints)
		
	
	s = scoreBasins(basinCollection)
	print("Score = {}".format(s))	

if __name__ == "__main__":
	main(sys.argv)
