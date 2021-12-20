#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def applyPointRotation( pt, rotationNumber):
	origX, origY, origZ = pt
	
	diceFace = rotationNumber % 4
	if (diceFace == 0):
		x = origX
		y = origY
		z = origZ
	elif (diceFace == 1):
		x = origZ
		y = origY
		z = -origX
	elif (diceFace == 2):
		x = origY
		y = origZ
		z = origX
	elif (diceFace == 3):
		x = origY
		y = -origZ
		z = -origX
	elif (diceFace == 4):
		x = -origZ
		y = origY
		z = origX
	else:
		x = -origX
		y = origY
		z = -origZ
	
	faceRot = rotationNumber // 6
	if faceRot == 0:
		frx = x
		fry = y
		frz = z
	elif faceRot == 1:
		frx = -y
		fry = x
		frz = z
	elif faceRot == 2:
		frx = -x
		fry = -y
		frz = z
	else:
		frx = y
		fry = -x
		frz = z
		
	return [frx, fry, frz]
	
	

def calcDist(pt1, pt2):
	# Returns (deltaX, deltaY, deltaZ, sumOfSqs)
	deltas = []
	sumOfSqs = 0
	for i in range(len(pt1)):
		dist = pt1[i] -pt2[i]
		deltas.append(dist)
		sumOfSqs += dist * dist
	return tuple(deltas + [sumOfSqs])

def insertDistInOrderedList(l, distData):
	# insert into nearbyBeacons list in order
	for i in range(len(l)):
		if l[i][3] > distData[3]:
			l.insert(i, distData)
			distData = None
			return
	
	if distData != None:
		# insert at the end
		l.append(distData)

class Beacon:
	def __init__(self, scannerId, beaconPos, nearbyBeacons):
		self.knownScanners = { scannerId: beaconPos }
		
		self.nearbyBeacons = []
		for eachBeacon in nearbyBeacons :
			distData = calcDist(beaconPos, eachBeacon)
			print("distData for beacon {} and {} = {}".format(beaconPos, eachBeacon, distData))
			insertDistInOrderedList(self.nearbyBeacons, distData)
			
					
		eprint("Beacon created for scanner ID {} with {} nearby".format(scannerId, len(self.nearbyBeacons)))
					
	def dump(self):
		eprint("    Known scanners:")
		for ks in self.knownScanners:
			eprint("      {}".format(ks))
		eprint("    Nearby beacons:")
		
		i = 0
		for nb in self.nearbyBeacons:
			eprint("      {}".format(nb))
			i += 1
			if i > 5:
				return
		
	def computeSimilarScore(self, otherBeacon):
		myDistData = self.nearbyBeacons
		rhsDistData = otherBeacon.nearbyBeacons[:]
		
		mySharedB = []
		rSharedB = []
		for myIdx in range(len(myDistData)):
			foundFlag = False
			for rIdx in range(len(rhsDistData)):
				myB = myDistData[myIdx]
				rB = rhsDistData[rIdx]
				if myB[3] == rB[3]:
					lRawDist = [ abs(x) for x in myB[:3] ]
					lRawDist.sort()
					rRawDist = [ abs(x) for x in rB[:3] ]
					rRawDist.sort()
					if rRawDist == lRawDist:
						mySharedB.append(myB)
						rSharedB.append(rB)
						del rhsDistData[rIdx]
						foundFlag = True
						
						
						break
			if foundFlag:
				continue
				
		#if (len(mySharedB)):
			
				
						
		return len(mySharedB)
		

class Scanner:
	def __init__(self, inputData):
		# First line should be "--- scanner ## ---"
		firstLineParts = inputData.pop(0).split()
		self.scannerId = int(firstLineParts[2])
		
		self.beaconCoords = []
		while len(inputData) > 0:
			beaconData = inputData.pop(0)
			
			if (beaconData == ""):
				break
				
			bc = [ int(x) for x in beaconData.split(",") ]
			eprint("beaconCoord = {}".format(bc))
			self.beaconCoords.append(bc)
			
		eprint("Created a scanner with {} beacons".format(len(self.beaconCoords)))
		
		self.beacons = []
		for i in range(len(self.beaconCoords)):
			copyOfBeacons = self.beaconCoords[:]
			curBPos = copyOfBeacons.pop(i)
			b = Beacon(self.scannerId, curBPos, copyOfBeacons)
			self.beacons.append(b)
			
	#def addBeacon(self, beaconCoord):
		

	def dump(self):
		eprint("--- scanner {} ---".format(self.scannerId))
		for i in range(len(self.beaconCoords)):
			coord = self.beaconCoords[i]
			eprint("  {},{},{}".format(*coord))
			eprint("  Beacon data:")
			self.beacons[i].dump()
			
	def findClosestScanner(self, listOfOtherScanners):
			# order scanners in order of most common beacons
			eprint("findClosestScanner({} scanners)".format(len(listOfOtherScanners)))
			osSharedList = []
			for os in listOfOtherScanners:
				ns = self.numberOfSharedBeacons(os)
				eprint("Number shared between {} and {} is {}".format(self.scannerId, os.scannerId, ns))
				osSharedList.append(ns)
			
			eprint("findClosestScanner summary: {}".format(osSharedList))
			maxShared = max(osSharedList)
			maxSharedIndex = osSharedList.index(maxShared)
			return listOfOtherScanners[maxSharedIndex]
			
	def numberOfSharedBeacons(self, otherScanner):
		fullMax = []
		eprint("numberOfSharedBeacons between scanners {} and {}".format(self.scannerId, otherScanner.scannerId))
		for b in self.beacons:
			numShared = []
			for ob in otherScanner.beacons:
				ss = b.computeSimilarScore(ob)
				numShared.append(ss)
			eprint("Max: {} from {}".format(max(numShared), numShared))
			fullMax.append(max(numShared))
		eprint("fullMax = {}".format(fullMax))
		
		countShared = 0
		for x in fullMax:
			if x > 5:
				countShared += 1
		return countShared

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	scannerList = []
	while(len(stringData) > 0):
		s = Scanner(stringData)
		scannerList.append(s)
		
		

	eprint("Created {} scanners".format(len(scannerList)))
	
	for s in scannerList:
		s.dump()
		
	cn = scannerList[0].findClosestScanner(scannerList[1:])
	eprint("Closest scanner is {}".format(cn.scannerId))
	
if __name__ == "__main__":
	main(sys.argv)
