#!/usr/bin/env python3

import sys

root_dir = {}

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def runTest(treeMap, x, y, xStart, yStart, xStep, yStep):
	eprint("runTest(treeMap, x={}, y={}, xStart={}, yStart={}, xStep={}, yStep={}".format(x, y, xStart, yStart, xStep, yStep))
	curX = xStart
	curY = yStart
	maxTree = -1
	while True:
		eprint("curX = {} curY = {}".format(curX, curY))
		curTree = int(treeMap[curY][curX])

		if xStep != 0:
			if curX == x:
				# reached test tree
				if (curTree > maxTree):
					eprint("Tree at {},{} is visible".format(x,y))
					return True
				else:
					eprint("Tree at {},{} is NOT visible".format(x,y))
					return False
			curX += xStep
		elif yStep != 0:
			if curY == y:
				if (curTree > maxTree):
					eprint("Tree at {},{} is visible".format(x,y))
					return True
				else:
					eprint("Tree at {},{} is NOT visible".format(x,y))
					return False
			curY += yStep
	
		if (curTree > maxTree):
			maxTree = curTree


def isVisible(treeMap, x, y):
	# From left
	if runTest(treeMap, x, y, 0, y, 1, 0):
		return True

	# From top
	if runTest(treeMap, x, y, x, 0, 0, 1):
		return True


	# From right
	if runTest(treeMap, x, y, len(treeMap[0])-1, y, -1, 0):
		return True


	# From bottom
	if runTest(treeMap, x, y, x, len(treeMap)-1, 0, -1):
		return True

	return False


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	numVisible = 0
	visiMap = []
	for y in range(len(data)):
		visiRow = ""
		for x in range(len(data[0])):
			if isVisible(data, x, y):
				numVisible += 1
				visiRow += "@"
			else:
				visiRow += "."
		visiMap.append(visiRow)

	for r in visiMap:
		eprint(r)


	print("Num visible = {}".format(numVisible))

if __name__ == "__main__":
	main(sys.argv)
