#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def minXPower(minXVal):
	minPower = 0
	xReach = 0
	while True:
		minPower += 1
		xReach += minPower
		
		if (xReach >= minXVal):
			return minPower

def isMiss(xTarget, yTarget, pos):
	if (pos[0] > xTarget[1]):
		return True
		
	if (pos[1] < yTarget[0]):
		return True
		
def isUndershot(xTarget, yTarget, path):
	for eachPt in path:
		if (eachPt[0] >= xTarget[0]) and (eachPt[1] >= yTarget[0]):
			return False
	return True
		
def isInTarget(xTarget, yTarget, pos):
	if ( xTarget[0] <= pos[0] <= xTarget[1] ):
		if ( yTarget[0] <= pos[1] <= yTarget[1] ):
			return True
	return False

def calcShot(xTarget, yTarget, v):
	'''
	xTarget and yTarget is 2 item list x range
	v is x,y tuple of muzzle velocity
	'''

	path = []
	steps = 0
	pos = (0,0)
	curV = v
	maxY = 0
	
	while not isMiss(xTarget, yTarget, pos):
		steps += 1
		pos = (pos[0] + curV[0], pos[1] + curV[1])
		
		if (pos[1] > maxY):
			maxY = pos[1]
			
		if (curV[0] > 0):
			curV = (curV[0] - 1, curV[1] - 1 )
		else:
			curV = (curV[0], curV[1] - 1 )
		
		path.append(pos)
		
		if isInTarget(xTarget, yTarget, pos):
			return True, pos, path, maxY
			
	return False, pos, path, maxY
	
def printShot(xTarget, yTarget, path):
	finalPos = path[-1]
	maxX = max(xTarget[1], finalPos[0])
	minY = min(yTarget[0], finalPos[1])
	
	allYs = [ pt[1] for pt in path ]
	maxY = max(allYs)
	
	eprint("X = 0 - {}".format(maxX))
	eprint("Y = {} - {}".format(minY, maxY))
	
	for y in range(maxY, minY - 1, -1):
		rowText = ""
		for x in range(maxX + 1):
			pt = (x,y)
			if (x == 0) and (y == 0):
				rowText += "S"
			elif (pt in path):
				rowText += '#'
			elif isInTarget(xTarget, yTarget, pt):
				rowText += "T"
			else:
				rowText += "."
		eprint(rowText)
			

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	xBegPos = stringData[0].index("=")
	xEndPos = stringData[0].index(",", xBegPos)
	xStr = stringData[0][xBegPos+1: xEndPos]
	eprint("xBegPos = {}, xEndPos = {}".format(xBegPos, xEndPos))
	eprint("xStr = {}".format(xStr))
	xComponents = xStr.split("..")
	eprint("xComp = {}".format(xComponents))
	
	yStr = stringData[0][xEndPos+1:]
	eprint("yStr = {}".format(yStr))
	yComponents = yStr[3:].split("..")
	eprint("yComp = {}".format(yComponents))
	
	xTarget = [ int(x) for x in xComponents ]
	yTarget = [ int(y) for y in yComponents ]
	
	eprint("X area = {}, and y area = {}".format(xTarget, yTarget))
	
	xMinPow = minXPower(xTarget[0])
	eprint("X min power = {}".format(xMinPow))
	
	mv = (6,3)
	
	eprint(calcShot(xTarget, yTarget, mv))
	
	success, finalPos, path, maxY = calcShot(xTarget, yTarget, mv)
	
	printShot(xTarget, yTarget, path)
	
	eprint("MaxY = {}".format(maxY))
	
	hits = 0
	allMaxY = 0
	for mvX in range(xMinPow, xTarget[1] + 1):
		for mvY in range(yTarget[0] - 1, abs(yTarget[0] * 10)):
			mv = (mvX, mvY)
			hit, finalPos, path, maxY = calcShot(xTarget, yTarget, mv)
			
			if hit:
				# Nice job, check maxY
				eprint("Hit with mv = {}".format(mv))
				#printShot(xTarget, yTarget, path)
				
				if (maxY > allMaxY):
					eprint("New max y = {}".format(maxY))
					allMaxY = maxY
					
				hits += 1
				
				
									
	eprint("Final solve: {}".format(allMaxY))
	eprint("Pt 2: {}".format(hits))
	
	
if __name__ == "__main__":
	main(sys.argv)
