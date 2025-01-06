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

	def rotateGuard(self):
		print(f"Rotating")
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
			if (self.getXY(nextX, nextY) == '#'):
				print(f"We are hitting an obstacle if we go to {nextX},{nextY}")
				self.rotateGuard()
			else:
				print(f"Moving forward to {nextX},{nextY}")
				emptySpaceFound = True
	
		self.guardX = nextX
		self.guardY = nextY

		if (not self.isGuardInBounds()):
			return False
		else:
			self.visitList.add( (self.guardX, self.guardY) )
			return True


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	lab = LabMap(data)
	keepMoving = True
	while(keepMoving):
		keepMoving = lab.moveGuardForward()
	
	part1 = lab.visitCount()
	print(f"Part 1 = {part1}")

if __name__ == "__main__":
	main(sys.argv)
