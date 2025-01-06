#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

class LabMap:
	def __init__(self, mapData):
		self.width = len(mapData[0])
		self.height = len(mapData)
		self.map = dict()
		self.visitList = set()
		for x in range(self.width):
			for y in range(self.height):
				if (mapData[y][x] != '.'):
					if (mapData[y][x] == '#'):
						self.map[ (x,y) ] = '#'
					else:
						print(f"Init map with guard at {x},{y}")
						self.guardX = x
						self.guardY = y
						self.guardDirection = (0,-1)
						self.visitList.add( (self.guardX, self.guardY) )

		self.origGuardX = self.guardX
		self.origGuardY = self.guardY
		self.origGuardDir = self.guardDirection
		self.history = []

	def resetGuard(self):
		self.guardX = self.origGuardX
		self.guardY = self.origGuardY
		self.guardDirection = self.origGuardDir
		self.visitList.clear()
		self.history.clear()

	def rotateGuard(self):
		#print(f"Rotating")
		rotateList = [ (1,0), (0,1), (-1,0), (0,-1) ]
		curIndex = rotateList.index(self.guardDirection)
		curIndex += 1
		curIndex %= 4
		self.guardDirection = rotateList[curIndex]

	def getXY(self, x: int, y: int) -> chr:
		return self.map.get( (x,y), '.')

	def printMap(self):
		print("Map:")
		for y in range(self.height):
			curRow = ''
			for x in range(self.width):
				curRow += self.getXY(x,y)
			print(curRow)

	def visitCount(self) -> int:
		return len(self.visitList)

	def isGuardInBounds(self) -> bool:
		if self.guardX < 0 or self.guardX >= self.width:
			return False
		if self.guardY < 0 or self.guardY >= self.height:
			return False
		return True

	def moveGuardForward(self):
		if (not self.isGuardInBounds()):
			return False

		emptySpaceFound = False
		while(emptySpaceFound == False):
			nextX = self.guardX + self.guardDirection[0]
			nextY = self.guardY + self.guardDirection[1]
			nextSpaceVal = self.getXY(nextX, nextY)
			if (nextSpaceVal == '#') or (nextSpaceVal == 'O'):
				#print(f"We are hitting an obstacle if we go to {nextX},{nextY}")
				self.rotateGuard()
			else:
				#print(f"Moving forward to {nextX},{nextY}")
				emptySpaceFound = True
	
		self.guardX = nextX
		self.guardY = nextY
		self.history.append( (self.guardX, self.guardY, self.guardDirection) )

		if (not self.isGuardInBounds()):
			return False
		else:
			self.visitList.add( (self.guardX, self.guardY) )
			return True

	def inLoop(self) -> bool:
		curHistoryVal = (self.guardX, self.guardY, self.guardDirection)
		if self.history.count(curHistoryVal) > 1:
			return True
		else:
			return False

	def doesThisMapLoop(self, obsX, obsY) -> bool:
		print(f"doesThisMapLoop({obsX}, {obsY})")
		loopFound = False
		keepMoving = True

		oldVal = self.getXY(obsX, obsY)
		if (oldVal == '#'):
			# Putting an obstruction where there already is one won't create a loop
			return False

		self.map[ (obsX,obsY) ] = 'O'

		while(keepMoving):
			keepMoving = self.moveGuardForward()
			if self.inLoop():
				loopFound = True
				keepMoving = False

		del self.map[ (obsX,obsY) ]
		self.resetGuard()

		print(f"  Returning from doesThisMapLoop({obsX}, {obsY}) with result {loopFound}")
		return loopFound

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	lab = LabMap(data)
	part2 = 0
	for x in range(lab.width):
		for y in range(lab.height):
			if lab.doesThisMapLoop(x,y):
				part2 += 1

	print(f"Part 2 = {part2}")

if __name__ == "__main__":
	main(sys.argv)
