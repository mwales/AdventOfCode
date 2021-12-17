#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getSize(mapStringData):
	x = len(mapStringData[0])
	y = len(mapStringData)
	return (x,y)
	
def printMapWithPath(mapData, mapSize, path, cd):
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
			
		rowText += "          "
		for x in range(mapSize[0]):
			if cd[(x,y)][0] == None:
				rowText += "None "
			else:
				rowText += "%4d " % cd[(x,y)][1]
				
				
		eprint(rowText)
		
def mapToDict(mapStringData):
	'''
	returns map with risk of each point
	returns cd with bestpath and lowestrisk to each point
	'''
	
	y = 0
	x = 0
	md = {}
	cd = {}
	for eachline in mapStringData:
		x = 0
		for eachchar in eachline:
			md[(x,y)] = int(eachchar)
			cd[(x,y)] = (None, None)
			x += 1
		y += 1
	return md, cd
	
	
def findNeighbors(mapData, mapSize, pos):
	retVal = set()
	(mx,my) = mapSize
	possibles = [ (pos[0] - 1, pos[1]),
	              (pos[0] + 1, pos[1]),
	              (pos[0],     pos[1] - 1),
	              (pos[0],     pos[1] + 1) ]
	#eprint("Possibles {}".format(possibles))
	
	for p in possibles:
		x,y = p
		#eprint("x = {}, y = {}".format(x,y))
		if (0 <= x < mx) and (0 <= y < my):
			retVal.add( (x,y) )
	return retVal
	
def findNextPath(mapData, mapSize, pathCurrent, oldRisk, cellData, maxDepth):
	'''
	Returns the path taken to the end and risk as tuple
	Determines current pos as last point in pathCurrent, adds our risk
	'''
	#eprint("findNextPath(md, ms, {}, {}, cd, {})".format(pathCurrent, oldRisk, maxDepth))
	#printMapWithPath(mapData, mapSize, pathCurrent, cellData)
	
	curPos = pathCurrent[-1]
	curRisk = mapData[curPos] + oldRisk
	
	# Do we already have a better path to the current cell?
	if (cellData[curPos] == (None, None)):
		cellData[curPos] = (pathCurrent, curRisk)
	else:
		cdBestPath, cdBestRisk = cellData[curPos]
		if cdBestRisk < curRisk:
			#eprint("This path already has better solution")
			# This is a bad solution, back away
			return None, None
		elif cdBestRisk > curRisk:
			#eprint("This path improves the celldata best path from {} to {}".format(cdBestRisk, curRisk))
			cellData[curPos] = (pathCurrent, curRisk)
			
	if (len(pathCurrent) == maxDepth):
		#eprint("Max depth reached")
		return None, None
	
	if (curPos == (mapSize[0] - 1, mapSize[1] - 1)):
		# End condition!
		eprint("Reached the goal!")
		return pathCurrent, curRisk
	
	nextMoves = findNeighbors(mapData, mapSize, curPos)
	#eprint("Raw next moves: {}".format(nextMoves))
	
	# eliminate places we have already been
	for breadcrumb in pathCurrent:
		if breadcrumb in nextMoves:
			nextMoves.remove(breadcrumb)
	#eprint("Without crumbs already: {}".format(nextMoves))
	
	if (len(nextMoves) == 0):
		# We are at a dead end
		#eprint("Dead end, no bueno")
		return None, None	
	
	# nextmoves should only have new positions to goto
	bestMove = None
	bestRisk = None
	for eachMov in nextMoves:
		#eprint("Trying {}...".format(eachMov))
		updatedPath = pathCurrent.copy()
		updatedPath.append(eachMov)
		fullBestPath, fullBestRisk = findNextPath(mapData, mapSize, updatedPath, curRisk, cellData, maxDepth)
		if (fullBestPath != None) and ((bestRisk == None) or (bestRisk > fullBestRisk)):
			bestMove = fullBestPath
			bestRisk = fullBestRisk
	
	return bestMove, bestRisk
	

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	eprint("Start solve")
	md, cd = mapToDict(stringData)
	ms = getSize(stringData)
	
	for maxdepth in range(5, 300, 5):
		print("maxdepth = {}".format(maxdepth))
		path, risk = findNextPath(md, ms, [ (0,0) ], 0, cd, maxdepth)
		print("P={}, R={}".format(path, risk))
		
		
		if (path != None):
			break
	
	eprint("Done: path = {}, risk= {}".format(path, risk))
	
	# fix for erroneously adding start pos
	eprint("risk = {}, md[(0,0)]={}".format(risk, md[(0,0)]))
	sol = risk - md[(0,0)]
	print("Solution = {}".format(sol))
	
if __name__ == "__main__":
	main(sys.argv)
