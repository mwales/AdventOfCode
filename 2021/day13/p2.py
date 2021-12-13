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
		print(rowText)
		
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
			
	printMap(mapData)
	print("FD = {}".format(foldData))
	
	for eachfold in foldData:
		if eachfold[0] == 'y':
			mapData = verticalFold(mapData, eachfold[1])
		else:
			mapData = horizontalFold(mapData, eachfold[1])
			
		print("Num dots after fold = {}".format(len(mapData)))
			
		printMap(mapData)
		
	print("Number set = {}".format(len(mapData)))
	
if __name__ == "__main__":
	main(sys.argv)
