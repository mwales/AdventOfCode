#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getHeight(x, y, mapData):
	#eprint("getHeight({},{})".format(x,y))
	return int(mapData[y][x])
	
def isPointLow(x, y, mapData):
	# Get our point
	pt = getHeight(x,y,mapData)
	
	# Check N
	if (y >= 1):
		if (pt >= getHeight(x, y-1, mapData)):
			return False
	
	# Check S
	if (y + 1 < len(mapData)):
		if (pt >= getHeight(x, y+1, mapData)):
			return False
	
	# Chech W
	if (x >= 1):
		if (pt >= getHeight(x - 1, y, mapData)):
			return False
	
	# Check E
	if ( x + 1 < len(mapData[0])):
		if (pt >= getHeight(x+1, y, mapData)):
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
