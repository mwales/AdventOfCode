#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def printMap(octos, size):
	for y in range(size[1]):
		text = ""
		for x in range(size[0]):
			text += str(octos[(x,y)])
		eprint(text)
		
def iterateMap(octos, size):
	flashMap = set()
	increasePts = []
	
	# Whole area should be iterated at least once
	for x in range(size[0]):
		for y in range(size[1]):
			increasePts.append((x,y))
			
	while (len(increasePts) > 0):
		#eprint("CheckMe = {}".format(increasePts))
		pt = increasePts.pop()
		octos[pt] += 1
		if (octos[pt] >= 10) and (pt not in flashMap):
			eprint("Flash at {}".format(pt))
			flashMap.add(pt)
			increasePts.extend(neighbors(size,pt))
			
	# Reset all flashed cells to zero
	for fc in flashMap:
		octos[fc] = 0
		
	return len(flashMap)	

def neighbors(size, point):
	retVal = []
	modPoints = []
	for xMod in range(-1, 2):
		for yMod in range(-1, 2):
			x = point[0] + xMod
			y = point[1] + yMod
			
			modPoints.append( (x,y) )
	
	# Don't add self
	modPoints.remove(point)

	ptsInRange = [ pt for pt in modPoints if (0 <= pt[0] < size[0]) and (0 <= pt[1] < size[1]) ]	
	return ptsInRange
	

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	octos = {}
	
	ms = (len(stringData[0]), len(stringData))
	
	for x in range(ms[0]):
		for y in range(ms[1]):
			octos[(x,y)] = int(stringData[y][x])
	
	printMap(octos, ms)
	
	totalFlashes = 0
	for i in range(100):
		f = iterateMap(octos, ms)
		totalFlashes += f
		
		eprint("After iteration {}".format(i+1))
		eprint("Flashes = {}, total flashes = {}".format(f, totalFlashes))
		printMap(octos, ms)
		
	print("Total flashes = {}".format(totalFlashes))
		
if __name__ == "__main__":
	main(sys.argv)
