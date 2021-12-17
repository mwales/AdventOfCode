#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getSize(mapStringData):
	x = len(mapStringData[0])
	y = len(mapStringData)
	return (x,y)
	
def printMapWithPath(mapData, mapSize, path):
	for y in range(mapSize[1]):
		rowText = ""
		for x in range(mapSize[0]):
			if (x,y) in path:
				i = path.index( (x,y) )
				if (i == (len(path) - 1)):
					rowText += 'X'
				else:
					rowText += "."
			else:
				rowText += str(mapData[(x,y)])
		eprint(rowText)
		
def mapToDict(mapStringData):
	y = 0
	x = 0
	retval = {}
	for eachline in mapStringData:
		x = 0
		for eachchar in eachline:
			retval[(x,y)] = int(eachchar)
			x += 1
		y += 1
	return retval
	
def findNeighbors(mapData, mapSize, pos):
	retVal = set()
	(mx,my) = mapSize
	possibles = [ (pos[0] - 1, pos[1]),
	              (pos[0] + 1, pos[1]),
	              (pos[0],     pos[1] - 1),
	              (pos[0],     pos[1] + 1) ]
	eprint("Possibles {}".format(possibles))
	
	for p in possibles:
		x,y = p
		eprint("x = {}, y = {}".format(x,y))
		if (0 <= x < mx) and (0 <= y < my):
			retVal.add( (x,y) )
	return retVal
	
def findNextPath(mapData, mapSize, pathCurrent, oldRisk):
	'''
	Returns the path taken to the end and risk as tuple
	Determines current pos as last point in pathCurrent, adds our risk
	'''
	eprint("findNextPath(md, ms, {}, {})".format(pathCurrent, oldRisk))
	printMapWithPath(mapData, mapSize, pathCurrent)
	
	curPos = pathCurrent[-1]
	curRisk = mapData[curPos] + oldRisk
	
	if (curPos == (mapSize[0] - 1, mapSize[1] - 1)):
		# End condition!
		eprint("Reached the goal!")
		return pathCurrent, curRisk
	
	nextMoves = findNeighbors(mapData, mapSize, curPos)
	eprint("Raw next moves: {}".format(nextMoves))
	
	# eliminate places we have already been
	for breadcrumb in pathCurrent:
		if breadcrumb in nextMoves:
			nextMoves.remove(breadcrumb)
	eprint("Without crumbs already: {}".format(nextMoves))
	
	if (len(nextMoves) == 0):
		# We are at a dead end
		eprint("Dead end, no bueno")
		return None, None	
	
	# nextmoves should only have new positions to goto
	bestMove = None
	bestRisk = None
	for eachMov in nextMoves:
		eprint("Trying {}...".format(eachMov))
		updatedPath = pathCurrent.copy()
		updatedPath.append(eachMov)
		fullBestPath, fullBestRisk = findNextPath(mapData, mapSize, updatedPath, curRisk)
		if (fullBestPath != None) and ((curRisk == None) or (curRisk > fullBestRisk)):
			bestMove = fullBestPath
			bestRisk = fullBestRisk
	
	return fullBestPath, fullBestRisk
	

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	eprint("Start solve")
	md = mapToDict(stringData)
	ms = getSize(stringData)
	path, risk = findNextPath(md, ms, [ (0,0) ], 0)
	
	eprint("Done: path = {}, risk= {}".format(path, risk))
	
if __name__ == "__main__":
	main(sys.argv)
