#!/usr/bin/env python3

import sys

root_dir = {}

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def runTest(treeMap, xStart, yStart, x, y, xStep, yStep):
	eprint("runTest(treeMap, x={}, y={}, xStart={}, yStart={}, xStep={}, yStep={}".format(x, y, xStart, yStart, xStep, yStep))
	curX = xStart
	curY = yStart
	maxTree = -1
	numVisi = 0
	ourHeight = int(treeMap[yStart][xStart])
	while True:
		eprint("curX = {} curY = {}, numVisi={}".format(curX, curY, numVisi))

		if xStep != 0:
			if curX == x:
				return numVisi
			curX += xStep
		elif yStep != 0:
			if curY == y:
				return numVisi
			curY += yStep

		curTree = int(treeMap[curY][curX])
		numVisi += 1

		if (curTree >= ourHeight):
			return numVisi



def scenicScore(treeMap, x, y):
	eprint("\nStarting score for {},{}".format(x,y))
	# From left
	endProduct = 1
	vl = runTest(treeMap, x, y, 0, y, -1, 0)
	vt = runTest(treeMap, x, y, x, 0, 0, -1)
	vr = runTest(treeMap, x, y, len(treeMap[0])-1, y, 1, 0)
	vd = runTest(treeMap, x, y, x, len(treeMap)-1, 0, 1)
	ss = vl * vt * vr * vd

	eprint("Scenic score for {},{} = {} * {} * {} * {} = {}".format(x, y, vl, vt, vr, vd, ss))
	return ss


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	maxScore = -1
	for y in range(1, len(data) - 1):
		for x in range(1, len(data[0]) - 1):
			ss = scenicScore(data, x, y)
			if ss > maxScore:
				maxScore = ss

	print("Max = {}".format(maxScore))

if __name__ == "__main__":
	main(sys.argv)
