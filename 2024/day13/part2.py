#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")


def addPts(pt0: tuple[int, int], pt1: tuple[int, int]) -> tuple[int,int]:
	retVal = ( pt0[0] + pt1[0], pt0[1] + pt1[1] )
	return retVal

def scalePt(pt: tuple[int, int], scalar: int) -> tuple[int, int]:
	retVal = ( pt[0] * scalar, pt[1] * scalar)
	return retVal

class Grid:
	def __init__(self, inputData: list[str]):
		self.height = len(inputData)
		self.width = len(inputData[0])

		self.gridData = dict()
		for y, rowData in enumerate(inputData):
			for x, cellVal in enumerate(rowData):
				self.gridData[ (x,y) ] = cellVal

	def isInGrid(self, pt: tuple[int,int] ) -> bool:
		x = pt[0]
		y = pt[1]
		if (x < 0) or (x >= self.width):
			return False

		if (y < 0) or (y >= self.height):
			return False

		return True

	def floodRegion(self, pt: tuple[int,int]) -> list[ tuple[int,int] ]:
		retVal = []
		visitList = [pt]
		historyList = []
		curVal = self.gridData[pt]
		neighbors = [ (-1,0), (0,-1), (1,0), (0,1) ]
		while (len(visitList) > 0):
			curPt = visitList.pop(0)
			historyList.append(curPt)

			if (self.gridData[curPt] != curVal):
				continue

			retVal.append(curPt)

			for direction in neighbors:
				neighPt = addPts(curPt, direction)
				if ( (self.isInGrid(neighPt)) and
				     (neighPt not in historyList) and 
				     (neighPt not in visitList) ):
					visitList.append(neighPt)
		
		return retVal

class PrizeMachine:
	def __init__(self, btnA, btnB, prize):
		
		btnAParts = btnA.replace(",","").split(" ")
		btnBParts = btnB.replace(",","").split(" ")
		self.btnADelta = ( int(btnAParts[2][2:]), int(btnAParts[3][2:]) )
		self.btnBDelta = ( int(btnBParts[2][2:]), int(btnBParts[3][2:]) )

		debug(f"A = {self.btnADelta} and B={self.btnBDelta}")

		debug(f"A = {btnAParts} and B = {btnBParts}")

		prizeParts = prize.replace(",","").replace("X=","").replace("Y=","").split()
		self.prizePt = ( int(prizeParts[1]), int(prizeParts[2]) )
		debug(f"prize = {self.prizePt}")

	def findAllCombos(self):
		comboList = []
		maxAPressesX = self.prizePt[0] // self.btnADelta[0]
		maxAPressesY = self.prizePt[1] // self.btnADelta[1]
		maxAPresses = max(maxAPressesX, maxAPressesY)

		curPt = (0,0)
		for aPresses in range(0, maxAPresses):
			curPt = scalePt(self.btnADelta, aPresses)
			deltaDiff = addPts(self.prizePt, scalePt(curPt, -1))

			deltaBModX = deltaDiff[0] % self.btnBDelta[0]
			deltaBModY = deltaDiff[1] % self.btnBDelta[1]
			bxPresses = deltaDiff[0] // self.btnBDelta[0]
			byPresses = deltaDiff[1] // self.btnBDelta[1]

			if (deltaBModX == 0 and deltaBModY == 0 and bxPresses == byPresses):
				comboList.append( (aPresses, bxPresses) )

		return comboList




	def findPrizeInteger(self):
		Px, Py = self.prizePt

		Ax, Ay = self.btnADelta
		Bx, By = self.btnBDelta

		Apresses = ( Px * By - Py * Bx ) // (Ax * By - Ay * Bx)
		Bpresses = ( Px - Apresses * Ax) // Bx
		debug(f"findPrizeInteger returning ({Apresses},{Bpresses})")
		return (Apresses, Bpresses)

	def findPrizeFloat(self):
		Px, Py = self.prizePt

		Ax, Ay = self.btnADelta
		Bx, By = self.btnBDelta

		Apresses = ( Px * By - Py * Bx ) / (Ax * By - Ay * Bx)
		Bpresses = ( Px - Apresses * Ax) / Bx
		debug(f"findPrizeFloat returning ({Apresses},{Bpresses})")
		return (Apresses, Bpresses)

	def findPrize(self):
		Ai,Bi = self.findPrizeInteger()
		Af,Bf = self.findPrizeFloat()

		diff = abs(Ai-Af) + abs(Bi-Bf)
		if (diff > 0.01):
			return (0,0)
		else:
			return (Ai,Bi)


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()


	part1 = 0
	for i in range(0, len(data), 4):
		pm = PrizeMachine(data[i], data[i+1], data[i+2])
		aPresses, bPresses = pm.findPrize()

		if aPresses == None:
			continue

		part1 += aPresses * 3 + bPresses

	print(f"Part 1 = {part1}")

	part2 = 0
	for i in range(0, len(data), 4):
		pm = PrizeMachine(data[i], data[i+1], data[i+2])
		pm.prizePt = addPts( pm.prizePt, (10000000000000,10000000000000) )
		aPresses, bPresses = pm.findPrize()

		if aPresses == None:
			continue

		part2 += aPresses * 3 + bPresses

	print(f"Part 2 = {part2}")


if __name__ == "__main__":
	main(sys.argv)
