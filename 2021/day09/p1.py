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
	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	w = len(filedata[0])
	h = len(filedata)
	
	solution = 0
	for x in range(w):
		for y in range(h):
			if isPointLow(x, y, filedata):
				ptHeight = getHeight(x, y, filedata)
				eprint("x = {}, y = {}, h = {}".format(x, y, ptHeight))
				solution += ptHeight + 1
				
	print("Solution = {}".format(solution))

if __name__ == "__main__":
	main(sys.argv)
