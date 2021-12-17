#!/usr/bin/env python3

import sys

class CellData:
	def __init__(self, x, y, weight):
		self.pos = (x,y)
		self.dist = None
		self.path = None
		self.weight = weight
		
	def updateNeighbors(self, mapSize, cd):
		eprint("updateNeighbors(ms, cd) for {}, with path = {}".format(self.pos, self.path))
		retval = []
		nlist = findNeighbors(mapSize, self.pos)
		for npos in nlist:
			n = cd[npos[1]][npos[0]]
			ndist = self.dist + n.weight
			if (n.dist == None) or (n.dist > ndist):
				# Update neighbor distance
				n.dist = ndist
				eprint("path = {}".format(n.path))
				eprint("path = {}, pathcopy = {}".format(self.path, self.path[:]))
				n.path = self.path[:]
				n.path.append(n.pos)
				eprint("setting path for {} to {}".format(n.pos, n.path))
				retval.append(n)
		return retval
	
	def __lt__(self, other):
		return self.dist < other.dist
		
	def toString(self):
		#eprint("toString(x={}, y={}, weight={}, dist={}".format(self.pos[0], self.pos[1], self.weight, self.dist))
		if self.dist == None:
			return "%2d [None]   " % (self.weight)
		else:
			return "%2d [%4d]   " % (self.weight, self.dist)

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getSize(mapStringData):
	x = len(mapStringData[0])
	y = len(mapStringData)
	return (x,y)
	
def printWeightMap(cellData, mapSize):
	for y in range(mapSize[1]):
		rowText = ""
		for x in range(mapSize[0]):
			rowText += cellData[y][x].toString()
			
		eprint(rowText)
		
def mapToCellData(mapStringData):
	'''
	returns dict of CellData
	'''
	retVal = []
	y = 0
	x = 0
	
	for eachline in mapStringData:
		x = 0
		row = []
		for eachchar in eachline:
			row.append(CellData(x,y,int(eachchar)))
			x += 1
		y += 1
		retVal.append(row)
	return retVal
	
	
def findNeighbors(mapSize, pos):
	retVal = []
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
			retVal.append( (x,y) )
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
	cd = mapToCellData(stringData)
	ms = getSize(stringData)
	
	printWeightMap(cd, ms)
	
	cd[0][0].dist = 0
	cd[0][0].path = [ (0,0) ]
	
	eprint("here we go")
	
	printWeightMap(cd, ms)
	
	eprint("Did it have a dist set?")
	
	workList = []
	workList.extend(cd[0][0].updateNeighbors(ms, cd))
	
	destination = cd[ms[1]-1][ms[0]-1]
	
	i = 0
	while True:
		i += 1
		#printWeightMap(cd, ms)
		
		workList.sort()
		
		ni = workList.pop(0)
		
		eprint("Iter {}, working {}".format(i, ni.pos))
		
		workList.extend(ni.updateNeighbors(ms, cd))
		
		if ni == destination:
			eprint("We made it to destination")
			break;
			
	eprint("Dest = {}".format(destination.toString()))
	
	'''for maxdepth in range(300, 302, 1):
		print("maxdepth = {}".format(maxdepth))
		path, risk = findNextPath(md, ms, [ (0,0) ], 0, cd, maxdepth)
		print("P={}, R={}".format(path, risk))
		
		
		if (path != None):
			break
	
	eprint("Done: path = {}, risk= {}".format(path, risk))
	
	# fix for erroneously adding start pos
	eprint("risk = {}, md[(0,0)]={}".format(risk, md[(0,0)]))
	sol = risk - md[(0,0)]
	print("Solution = {}".format(sol))'''
	
if __name__ == "__main__":
	main(sys.argv)
