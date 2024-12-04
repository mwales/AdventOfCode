#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
		sys.stderr.write(f"{msg}\n")


class WordSearch:
	def __init__(self, gridData):
		self.grid = dict()
		self.width = len(gridData[0])
		self.height = len(gridData)
		for y in range(self.height):
			for x in range(self.width):
				self.grid[ (x,y) ] = gridData[y][x]

	def isWord(self, x, y, searchTerm, direction):
		curX = x
		curY = y
		for letterPos in range(len(searchTerm)):
			if (curX < 0) or (curX >= self.width):
				return False

			if (curY < 0) or (curY >= self.height):
				return False

			if (self.grid[(curX,curY)] != searchTerm[letterPos]):
				return False

			curX += direction[0]
			curY += direction[1]

		debug(f"Found {searchTerm} at {x},{y} using dir {direction}")
		return True


	def findWord(self, searchTerm):
		directionIncList = [ (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1) ]

		wc = 0
		for x in range(self.width):
			for y in range(self.height):
				for direction in directionIncList:
					if self.isWord(x,y,searchTerm,direction):
						wc += 1

		return wc
	
	def findWordsPart2(self):

		searchPattList1 = [ (0,0,1,1), (2,2,-1,-1) ]
		searchPattList2 = [ (0,2,1,-1), (2,0,-1,1) ]
		wc = 0
		for x in range(self.width):
			for y in range(self.height):
				for sp1 in searchPattList1:
					for sp2 in searchPattList2:
						if ( self.isWord(x + sp1[0],y + sp1[1],"MAS", (sp1[2], sp1[3]) ) and 
						     self.isWord(x + sp2[0],y + sp2[1],"MAS", (sp2[2], sp2[3]) ) ):
							wc += 1

		return wc
	

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	ws = WordSearch(data)
	part1 = ws.findWord("XMAS")
	print(f"Part1 = {part1}")

	part2 = ws.findWordsPart2()
	print(f"Part2 = {part2}")

if __name__ == "__main__":
	main(sys.argv)
