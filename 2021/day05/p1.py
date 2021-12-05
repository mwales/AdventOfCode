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
		eprint(eachLine)
		(x1,y1,x2,y2) = [int(x) for x in eachLine.split(",")]
		
		eprint("{} {} {} {}".format(x1, y1, x2, y2))
		pointData.append( (x1, y1, x2, y2) )
		
	print (pointData)
	
	mapData = {}
	
	# go through each line, and add a value for each spot on map
	for eachLine in pointData:
		(x1, y1, x2, y2) = eachLine
		if (y1 == y2):
			# horizontal line
			begX = min(x1, x2)
			endX = max(x1, x2)
			for x in range(begX, endX + 1):
				val = mapData.get( (x,y1), 0)
				val += 1
				mapData[(x,y1)] = val
		elif (x1 == x2):
			# vertical line
			begY = min(y1, y2)
			endY = max(y1, y2)
			for y in range(begY, endY + 1):
				val = mapData.get( (x1,y), 0)
				val += 1
				mapData[(x1,y)] = val
				
	print(mapData)
	
	p1 = 0
	for loc in mapData:
		print("{} = {}".format(loc, mapData[loc]))
		if mapData[loc] >= 2:
			p1 += 1
			
	print("p1 = {}".format(p1))

if __name__ == "__main__":
	main(sys.argv)
