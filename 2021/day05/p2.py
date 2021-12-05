#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	pointData = []
	for eachLine in filedata:
		arrowIndex = eachLine.index("->")
		eachLine = eachLine[:arrowIndex] + "," + eachLine[arrowIndex + 2:]
		(x1,y1,x2,y2) = [int(x) for x in eachLine.split(",")]
		pointData.append( (x1, y1, x2, y2) )
		
	#eprint (pointData)
	
	mapData = {}
	
	# go through each line, and add a value for each spot on map
	for eachLine in pointData:
		(x1, y1, x2, y2) = eachLine
		
		# Calc iteration deltas
		if (x1 < x2):
			deltaX = 1
		elif (x1 > x2):
			deltaX = -1
		else:
			deltaX = 0
			
		if (y1 < y2):
			deltaY = 1
		elif (y1 > y2):
			deltaY = -1
		else:
			deltaY = 0
			
		# Iterate through all the points on the line till end point
		i = 0
		while True:
			y = y1 + i * deltaY
			x = x1 + i * deltaX
			val = mapData.get( (x,y), 0)
			val += 1
			mapData[(x,y)] = val
			i += 1
			
			if ( (x == x2) and (y == y2) ):
				break;
			
				
	#eprint(mapData)
	
	p1 = 0
	for loc in mapData:
		#eprint("Location {} = {}".format(loc, mapData[loc]))
		if mapData[loc] >= 2:
			p1 += 1
			
	print("p2 = {}".format(p1))

if __name__ == "__main__":
	main(sys.argv)
