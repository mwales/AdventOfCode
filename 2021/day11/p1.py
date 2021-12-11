#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def printMap(octos, size):
	for y in range(size[1]):
		text = ""
		for x in range(size[0]):
			text += str(octos[(x,y)])
		print(text)
		
def iterateMap(octos, size):
	flashMap = set()
	checkMe = []
	
	for x in range(size[0]):
		for y in range(size[1]):
			octos[(x,y)] += 1
			
			if (octos[(x,y)] >= 10):
				eprint("{} flashing in first loop".format((x,y)))
				flashMap.add((x,y))
				checkMe.extend(neighbors(size, (x,y)))
				
	
			
	
	while (len(checkMe) > 0):
		print("CheckMe = {}".format(checkMe))
		pt = checkMe.pop()
		print("Checking {}".format(pt))
		octos[pt] += 1
		if (octos[pt] >= 10) and (pt not in flashMap):
			eprint("Additional flash at {}".format(pt))
			flashMap.add(pt)
			checkMe.extend(neighbors(size,pt))
			
	# Reset all flashed cells to zero
	for fc in flashMap:
		octos[fc] = 0
		
	return len(flashMap)
	
	

def neighbors(size, point):
	retVal = []
	for xMod in range(-1, 2):
		for yMod in range(-1, 2):
			x = point[0] + xMod
			y = point[1] + yMod
			# Filter out bad ones
			if (x < 0) or (y < 0):
				continue
			if (x,y) == point:
				continue; # not self
			if (x >= size[0]) or (y >= size[1]):
				continue
				
			retVal.append( (x,y) )
	return retVal
	

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
	firstFullFlash = None
	for i in range(100):
		f = iterateMap(octos, ms)
		totalFlashes += f
		
		if (f == ms[0] * ms[1]):
			eprint("Full flash at iter = {}".format(i + 1))
			if (firstFullFlash == None):
				firstFullFlash = i+1
		eprint("After iteration {}".format(i+1))
		eprint("Flashes = {}, total flashes = {}".format(f, totalFlashes))
		printMap(octos, ms)
		print("First Flash = {}".format(firstFullFlash))
	
if __name__ == "__main__":
	main(sys.argv)
