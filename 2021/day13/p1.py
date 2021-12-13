#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getMapDimensions(md):
	maxX = 0
	maxY = 0
	for x,y in md:
		if x > maxX:
			maxX = x
		if y > maxY:
			maxY = y
	return maxX, maxY
	
def printMap(md):
	maxX, maxY = getMapDimensions(md)
	
	for y in range(maxY+1):
		rowText = ""
		for x in range(maxX + 1):
			if (x,y) in md:
				rowText += '#'
			else:
				rowText += '.'
		eprint(rowText)
		
def verticalFold(md, row):
	eprint("Vertical fold at {}".format(row))
	newMap = set()
	for x,y in md:
		if y < row:
			newMap.add( (x,y) )
		elif y > row:
			yt = row - (y - row)
			newMap.add( (x,yt) )
	return newMap
	
def horizontalFold(md, col):
	eprint("Horizontal fold at {}".format(col))
	newMap = set()
	for x,y in md:
		if x < col:
			newMap.add( (x,y) )
		elif x > col:
			xt = col - (x - col)
			newMap.add( (xt,y) )
	return newMap
	
def fold(md, fold):
	# mapdata is a set of (x,y), (x or y, row/col)
	if fold[0] == 'y':
		md = verticalFold(md, fold[1])
	else:
		md = horizontalFold(md, fold[1])
	return md
	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	mapData = set()
	foldData = []
	inputMode = 0
	for sl in stringData:
		if sl == "":
			inputMode = 1
			continue
			
		if inputMode == 0:
			# Getting data points
			x,y = sl.split(',')
			mapData.add( (int(x),int(y)) )			
		else:
			# Getting fold data
			eprint("Fold: {}".format(sl))
			words = sl.split(' ')
			fd = words[2].split('=')
			eprint(fd)
			foldData.append( (fd[0], int(fd[1])) )

	eprint("Initial map")
	printMap(mapData)
	#eprint("FD = {}".format(foldData))
	
	mapData = fold(mapData, foldData[0])

	printMap(mapData)
	print("Num dots after fold = {}".format(len(mapData)))
	
	
if __name__ == "__main__":
	main(sys.argv)
