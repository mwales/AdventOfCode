#!/usr/bin/env python3

import sys
import copy

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

class CellMap:
	def __init__(self, data):
		self.mapData = data
		self.mapWidth = len(data[0])
		self.mapHeight = len(data)

	def getHeight(self, coord):
		letterOnMap = self.mapData[coord[1]][coord[0]]
		if (letterOnMap == 'S'):
			return 0
		elif (letterOnMap == 'E'):
			return ord('z') - ord('a')
		else:
			return ord(letterOnMap) - ord('a')

	def getPossibleMoves(self, coord):
		possibleCoords = { "^":(coord[0], coord[1]-1), "V":(coord[0], coord[1]+1),
		                   "<":(coord[0] - 1, coord[1]), ">":(coord[0] + 1, coord[1]) }

		retVal = dict()
		for pcPair in possibleCoords.keys():
			pc = possibleCoords[pcPair]
			if (pc[0] < 0) or (pc[0] >= self.mapWidth):
				continue
			if (pc[1] < 0) or (pc[1] >= self.mapHeight):
				continue
			elif (self.getHeight(pc) - 1) > self.getHeight(coord):
				continue
			else:
				retVal[pcPair] = possibleCoords[pcPair]

		return retVal

	def getStartPosition(self):
		for y in range(len(self.mapData)):
			for x in range(len(self.mapData[y])):
				if self.mapData[y][x] == 'S':
					return (x,y)
		else:
			eprint("Can't find the start")
			return None

	def getEndPosition(self):
		for y in range(len(self.mapData)):
			for x in range(len(self.mapData[y])):
				if self.mapData[y][x] == 'E':
					return (x,y)
		else:
			eprint("Can't find the end")
			return None



class ElfPath:
	def __init__(self, mapdata, breadcrumbs, pos):
		self.mapData = mapdata
		self.breadcrumbs = breadcrumbs
		self.pos = pos
		self.atGoal = self.pos == self.mapData.getEndPosition()
		self.spCache = -1

		self.printMap()

	def getNextMoves(self):
		if self.atGoal:
			return None

		possibleMoves = self.mapData.getPossibleMoves(self.pos)
		newPaths = []
		for direction in possibleMoves.keys():
			pm = possibleMoves[direction]
			if pm in self.breadcrumbs:
				continue
			newBc = copy.deepcopy(self.breadcrumbs)
			newBc[self.pos] = direction
			np = ElfPath(self.mapData, newBc, pm)
			newPaths.append(np)

		return newPaths

	def getShortestPathToGoal(self):
		if self.atGoal:
			return self

		if self.spCache != -1:
			return self.spCache

		possiblePaths = self.getNextMoves()
		if (len(possiblePaths) == 0):
			return None

		sp = None
		for pp in possiblePaths:
			if (pp.getShortestPathToGoal() == None):
				continue
			if (sp == None):
				sp = pp.getShortestPathToGoal()
			elif (sp.getShortestPathToGoal().pathLen() > pp.getShortestPathToGoal().pathLen()):
				sp = pp

		self.spCache = sp
		return sp

	def pathLen(self):
		return len(self.breadcrumbs)


	def atGoal(self):
		return self.atGoal


	def printMap(self):
		eprint("================== MAP =====================")

		for y in range(self.mapData.mapHeight):
			curRow = ""
			for x  in range(self.mapData.mapWidth):
				curCell = self.mapData.mapData[y][x]
				if (x,y) in self.breadcrumbs:
					curCell = self.breadcrumbs[ (x,y) ]
				if (x,y) == self.pos:
					curCell = "*"
				curRow += curCell

			eprint(curRow)
	
	
		

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	cm = CellMap(data)
	eprint("Dimensions: {} x {}".format(cm.mapWidth, cm.mapHeight))
	eprint("Start pos: {}".format(cm.getStartPosition()))
	eprint("End pos: {}".format(cm.getEndPosition()))

	bc = dict()
	pos = cm.getStartPosition()

	ep = ElfPath(cm,bc,pos)
	ep.getShortestPathToGoal()


if __name__ == "__main__":
	main(sys.argv)
