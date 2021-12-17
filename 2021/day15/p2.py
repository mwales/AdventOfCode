#!/usr/bin/env python3

import sys
import copy

class CellData:
	def __init__(self, x, y, weight):
		self.pos = (x,y)
		self.dist = None
		self.path = None
		self.weight = weight
		
	def updateNeighbors(self, mapSize, cd):
		#eprint("updateNeighbors(ms, cd) for {}, with path = {}".format(self.pos, self.path))
		retval = []
		nlist = findNeighbors(mapSize, self.pos)
		for npos in nlist:
			n = getCell(cd, npos)
			ndist = self.dist + n.weight
			if (n.dist == None) or (n.dist > ndist):
				# Update neighbor distance
				n.dist = ndist
				#eprint("path = {}".format(n.path))
				#eprint("path = {}, pathcopy = {}".format(self.path, self.path[:]))
				n.path = self.path[:]
				n.path.append(n.pos)
				#eprint("setting path for {} to {}".format(n.pos, n.path))
				retval.append(n)
		return retval
	
	def __lt__(self, other):
		return self.dist < other.dist
		
	def toString(self):
		#eprint("toString(x={}, y={}, weight={}, dist={}".format(self.pos[0], self.pos[1], self.weight, self.dist))
		if self.dist == None:
			return "%2d [None] " % (self.weight) + str(self.pos) + "   "
		else:
			return "%2d [%4d] " % (self.weight, self.dist) + str(self.pos) + "   "

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getSize(cd):
	x = len(cd[0])
	y = len(cd)
	return (x,y)
	
def printCellMap(cellData):
	for y in cellData:
		rowText = ""
		for x in y:
			rowText += x.toString()
			
		eprint(rowText)
		
def printWeightData(wd):
	for y in wd:
		rowText = ""
		for x in y:
			rowText += str(x) + " "
			
		eprint(rowText)
		
def stringToWeightData(mapStringData):
	retVal = []
	for eachline in mapStringData:
		row = []
		for eachchar in eachline:
			row.append(int(eachchar))
		retVal.append(row)
	return retVal

def weightDataToCellData(wd):
	retVal = []
	for y in range(len(wd)):
		row = []
		for x in range(len(wd[y])):
			row.append(CellData(x,y,wd[y][x]))
		retVal.append(row)
	return retVal
		


def getCell(cellData, pos):
	return cellData[pos[1]][pos[0]]

def addToAll(matrix, addVal):
	(xs,ys) = getSize(matrix)
	for x in range(xs):
		for y in range(ys):
			for s in range(addVal):
				matrix[y][x] += 1
				if matrix[y][x] == 10:
					matrix[y][x] = 1
					
def addToRight(leftMatrix, rightMatrix):
	# pos is all screwed up, so reinit
	for r in range(len(leftMatrix)):
		#eprint("loop")
		#printWeightData(leftMatrix)
		#xToAdd = 0
		#newXPos = len(leftMatrix[r])
		#for newItem in rightMatrix[r]:
			# Add the cell to the end of the left matrix
		leftMatrix[r].extend(rightMatrix[r][:])
		#printWeightData(leftMatrix)

def addToBottom(topMatrix, bottomMatrix):
	# pos is all screwed up, so reinit
	eprint("addToBottom called with matrix sizes of {}x{} and {}x{}".format(len(topMatrix[0]), len(topMatrix), len(bottomMatrix[0]), len(bottomMatrix)))
	'''numRowsToCopy = len(bottomMatrix)
	
	newRowCollection = []
	for r in range(numRowsToCopy):
		
		newRow = []
		for newItem in bottomMatrix[r]:
			# Add the cell to the end of the left matrix
			newRow.append(newItem)
			
			# Update the pos of the new cell
			#newItem.pos = (newItem.pos[0], newItem.pos[1] + len(topMatrix))
		
		newRowCollection.append(newRow)
	topMatrix.extend(newRowCollection)
	'''
	for row in bottomMatrix:
		topMatrix.append(row[:])

		
def copyCells(cellData):
	retVal = []
	for row in cellData:
		newRowData = []
		for col in row:
			newRowData.append(col.copy())
		retVal.append(newRowData)
	return retVal
	





def reinitMatrix(cd):
	y = 0
	for row in cd:
		x = 0
		for col in row:
			col.pos = (x,y)
			col.path = None
			col.dist = None
			x += 1
		y += 1
	
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

def solveMap(cd):
	reinitMatrix(cd)
	
	startPoint = getCell(cd, (0,0))
	startPoint.dist = 0
	startPoint.path = [ (0,0) ]
	
	eprint("Solving...")
	ms = getSize(cd)
	printWeightData(cd)
	
	#eprint("Did it have a dist set?")
	
	workList = []
	workList.extend(startPoint.updateNeighbors(ms, cd))
	
	destination = getCell(cd, (ms[0]-1, ms[1]-1))	
	
	i = 0
	while True:
		i += 1
		#printWeightMap(cd)
		
		workList.sort()
		
		ni = workList.pop(0)
		
		#eprint("Iter {}, working {}".format(i, ni.pos))
		
		workList.extend(ni.updateNeighbors(ms, cd))
		
		if ni == destination:
			eprint("We made it to destination")
			break;
			
	print("Dest = {}".format(destination.toString()))

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	wd = stringToWeightData(stringData)
	
	'''
	# part 1
	cd = weightDataToCellData(wd)
	solveMap(cd)
	
	return
	'''

	eprint("Extended cell")
	extendedCell = copy.deepcopy(wd)
	printWeightData(extendedCell)
	
	eprint("WD map:")
	printWeightData(wd)
	
	
	for i in range(4):
		#extendedCell = copy.deepcopy(wd)
		
		eprint("Added 1 to all")
		addToAll(extendedCell, 1)
		printWeightData(extendedCell)
		
		addToRight(wd, extendedCell)
		print("Iteration {}".format(i))
		printWeightData(wd)

	eprint("Final")

	printWeightData(wd)
	
	eprint("Time to start adding bottom rows")

	
	
	extendedCell = copy.deepcopy(wd)
	
	for i in range(4):
		eprint("Add bottom loop:")
		addToAll(extendedCell, 1)
		eprint("After adding 1 to everything")
		printWeightData(extendedCell)
		eprint("Adding...")
		addToBottom(wd, extendedCell)
		printWeightData(wd)
		
	
	eprint("all done")
	
	printWeightData(wd)
	
	cd = weightDataToCellData(wd)
	solveMap(cd)
	
	
	

	
if __name__ == "__main__":
	main(sys.argv)
