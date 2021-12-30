#!/usr/bin/env python3

import sys
import numpy


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
transforms = [    [ [ 1, 0, 0], [0, 1, 0], [0, 0, 1] ],
                  [ [ 1, 0, 0], [0, -1, 0], [0, 0, 1] ],
                  [ [ 1, 0, 0], [0, 1, 0], [0, 0, -1] ],
                  [ [ 1, 0, 0], [0, -1, 0], [0, 0, -1] ],

                  [ [ -1, 0, 0], [0, 1, 0], [0, 0, 1] ],
                  [ [ -1, 0, 0], [0, -1, 0], [0, 0, 1] ],
                  [ [ -1, 0, 0], [0, 1, 0], [0, 0, -1] ],
                  [ [ -1, 0, 0], [0, -1, 0], [0, 0, -1] ],

                  [ [ 1, 0, 0], [0, 0, 1], [0, 1, 0] ],
                  [ [ 1, 0, 0], [0, 0, -1], [0, 1, 0] ],
                  [ [ 1, 0, 0], [0, 0, 1], [0, -1, 0] ],
                  [ [ 1, 0, 0], [0, 0, -1], [0, -1, 0] ],

                  [ [ -1, 0, 0], [0, 0, 1], [0, 1, 0] ],
                  [ [ -1, 0, 0], [0, 0, -1], [0, 1, 0] ],
                  [ [ -1, 0, 0], [0, 0, 1], [0, -1, 0] ],
                  [ [ -1, 0, 0], [0, 0, -1], [0, -1, 0] ],


                  [ [ 0 , 1, 0], [1, 0, 0], [0, 0, 1] ],
                  [ [ 0 , 1, 0], [-1, 0, 0], [0, 0, 1] ],
                  [ [ 0 , 1, 0], [1, 0, 0], [0, 0, -1] ],
                  [ [ 0 , 1, 0], [-1, 0, 0], [0, 0, -1] ],
                  
                  [ [ 0 , -1, 0], [1, 0, 0], [0, 0, 1] ],
                  [ [ 0 , -1, 0], [-1, 0, 0], [0, 0, 1] ],
                  [ [ 0 , -1, 0], [1, 0, 0], [0, 0, -1] ],
                  [ [ 0 , -1, 0], [-1, 0, 0], [0, 0, -1] ],

                  [ [ 0, 1, 0], [0, 0, 1], [1, 0, 0] ],
                  [ [ 0, 1, 0], [0, 0, -1], [1, 0, 0] ],
                  [ [ 0, 1, 0], [0, 0, 1], [-1, 0, 0] ],
                  [ [ 0, 1, 0], [0, 0, -1], [-1, 0, 0] ],
                  
                  [ [ 0, -1, 0], [0, 0, 1], [1, 0, 0] ],
                  [ [ 0, -1, 0], [0, 0, -1], [1, 0, 0] ],
                  [ [ 0, -1, 0], [0, 0, 1], [-1, 0, 0] ],
                  [ [ 0, -1, 0], [0, 0, -1], [-1, 0, 0] ],


                  [ [ 0, 0, 1], [1, 0, 0], [0, 1, 0] ],
                  [ [ 0, 0, 1], [-1, 0, 0], [0, 1, 0] ],
                  [ [ 0, 0, 1], [1, 0, 0], [0, -1, 0] ],
                  [ [ 0, 0, 1], [-1, 0, 0], [0, -1, 0] ],
                  
                  [ [ 0, 0, -1], [1, 0, 0], [0, 1, 0] ],
                  [ [ 0, 0, -1], [-1, 0, 0], [0, 1, 0] ],
                  [ [ 0, 0, -1], [1, 0, 0], [0, -1, 0] ],
                  [ [ 0, 0, -1], [-1, 0, 0], [0, -1, 0] ],

                  [ [ 0, 0, 1], [0, 1, 0], [1, 0, 0] ],
                  [ [ 0, 0, 1], [0, -1, 0], [1, 0, 0] ],
                  [ [ 0, 0, 1], [0, 1, 0], [-1, 0, 0] ],
                  [ [ 0, 0, 1], [0, -1, 0], [-1, 0, 0] ],
                  
                  [ [ 0, 0, -1], [0, 1, 0], [1, 0, 0] ],
                  [ [ 0, 0, -1], [0, -1, 0], [1, 0, 0] ],
                  [ [ 0, 0, -1], [0, 1, 0], [-1, 0, 0] ],
                  [ [ 0, 0, -1], [0, -1, 0], [-1, 0, 0] ] ]



def applyPointRotation(pt, rotationNumber):
	rotTrans = transforms[rotationNumber]
	
	tPtNpa = numpy.dot(pt, rotTrans)
	tPt = [ x for x in tPtNpa ]
	
	#eprint("pt={}, rot={}, trans={}, retVal={}".format(pt, rotationNumber, rotTrans, tPt))
	#eprint("type compare. pt={}, retVal={}".format( type(pt), type(tPt)))
	return tPt

def vecAdd(vec1, vec2):
	retVal = []
	for i in range(len(vec1)):
		retVal.append(vec1[i] + vec2[i])
	return retVal
	
def vecDifference(vec1, vec2):
	retVal = []
	for i in range(len(vec1)):
		retVal.append(vec1[i] - vec2[i])
	return retVal
	
def listMode(l):
	curMaxIdx = 0
	curMaxCount = 0
	for i in range(len(l)):
		c = 0
		for item in l:
			if item == l[i]:
				c += 1
		
		if c > curMaxCount:
			curMaxCount = c
			curMaxIdx = i
	return l[curMaxIdx]

	
def applyPointRotation1( pt, rotationNumber):
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
		self.pos = beaconPos
		self.scannerId = scannerId
		
		self.nearbyBeacons = []
		for eachBeacon in nearbyBeacons :
			distData = calcDist(beaconPos, eachBeacon)
			#print("distData for beacon {} and {} = {}".format(beaconPos, eachBeacon, distData))
			insertDistInOrderedList(self.nearbyBeacons, distData)
			
					
		#eprint("Beacon created for scanner ID {} with {} nearby".format(scannerId, len(self.nearbyBeacons)))
					
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
		#eprint("computeSimilarScore(ob={} from scanner ID {}), we are {} for scanner ID".format(
		#       self.pos, self.scannerId, otherBeacon.pos, otherBeacon.scannerId))
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
						'''eprint("Scanner {} beacon {} == Scanner {} beacon {}".format(self.scannerId,
						                                                             mySharedB,
						                                                             otherBeacon.scannerId,
						                                                             rSharedB))'''
						mySharedB.append(myB)
						rSharedB.append(rB)
						del rhsDistData[rIdx]
						foundFlag = True
						
						
						break
			if foundFlag:
				continue
				
		#if (len(mySharedB)):
			
				
		#eprint("Returning similar score of {}".format(len(mySharedB)))
		return len(mySharedB)
		
	def computeIdenticalScore(self, otherBeacon):
		myDistData = self.nearbyBeacons
		rhsDistData = otherBeacon.nearbyBeacons[:]
		
		mySharedB = []
		rSharedB = []
		for myIdx in range(len(myDistData)):
			foundFlag = False
			for rIdx in range(len(rhsDistData)):
				myB = myDistData[myIdx]
				rB = rhsDistData[rIdx]
				if myB == rB:
					mySharedB.append(myB)
					rSharedB.append(rB)
					del rhsDistData[rIdx]
					foundFlag = True
					break
			if foundFlag:
				continue
				
		#if (len(mySharedB)):
		return len(mySharedB)
		
'''	def rotateOtherBeaconAndCheckForIdenticals(self, otherBeacon, rotationNum):
		myDistData = self.nearbyBeacons
		
		rhsDistDataUnrotated = otherBeacon.nearbyBeacons[:]
		rhsBeaconPos = applyPointRotation( otherBeacon.pos, rotationNum)
		for nonrot in rhsDistDataUnrotated:
			rhsDistData.append( 
'''

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
		
		# Copy the original coords so we can do rotations later on from these
		self.origBeaconCoords = self.beaconCoords[:]
		
		self.createBeaconList()
		
		self.pos = None
		
		'''
		self.beacons = []
		for i in range(len(self.beaconCoords)):
			copyOfBeacons = self.beaconCoords[:]
			curBPos = copyOfBeacons.pop(i)
			b = Beacon(self.scannerId, curBPos, copyOfBeacons)
			self.beacons.append(b)
		'''
			
	#def addBeacon(self, beaconCoord):
	def createBeaconList(self):
		self.beacons = []
		for i in range(len(self.beaconCoords)):
			copyOfBeacons = self.beaconCoords[:]
			curBPos = copyOfBeacons.pop(i)
			b = Beacon(self.scannerId, curBPos, copyOfBeacons)
			self.beacons.append(b)

	def dump(self):
		eprint("--- scanner {} ---".format(self.scannerId))
		eprint("  Orig Coords:")
		for b in self.origBeaconCoords:
			eprint("  {},{},{}".format(*b))
		
		eprint("  Rotated Coords:")
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
			
			if maxShared < 5:
				return None
			else:
				maxSharedIndex = osSharedList.index(maxShared)
				return listOfOtherScanners[maxSharedIndex]
			
	def numberOfSharedBeacons(self, otherScanner):
		fullMax = []
		#eprint("numberOfSharedBeacons between scanners {} and {}".format(self.scannerId, otherScanner.scannerId))
		for b in self.beacons:
			numShared = []
			for ob in otherScanner.beacons:
				ss = b.computeSimilarScore(ob)
				numShared.append(ss)
			#eprint("Max: {} from {}".format(max(numShared), numShared))
			fullMax.append(max(numShared))
		#eprint("fullMax = {}".format(fullMax))
		
		countShared = 0
		for x in fullMax:
			if x > 5:
				countShared += 1
		return countShared
		
	def numberOfIdenticalBeacons(self, otherScanner):
		fullMax = []
		#eprint("numberOfIdenticalBeacons between scanners {} and {}".format(self.scannerId, otherScanner.scannerId))
		for b in self.beacons:
			numShared = []
			for ob in otherScanner.beacons:
				ss = b.computeIdenticalScore(ob)
				numShared.append(ss)
			#eprint("Max: {} from {}".format(max(numShared), numShared))
			fullMax.append(max(numShared))
		#eprint("fullMax = {}".format(fullMax))
		
		countShared = 0
		for x in fullMax:
			if x > 5:
				countShared += 1
		return countShared
		
	def determineScannerPos(self, otherScanner):
		calcPositions = []
		eprint("determineScannerPos between scanners {} and {}".format(self.scannerId, otherScanner.scannerId))
		for b in self.beacons:
			numShared = []
			for ob in otherScanner.beacons:
				ss = b.computeIdenticalScore(ob)
				
				if ss > 5:
					# This is the same beacon, use it to determine scanner position
					calcPos = vecDifference( vecAdd(otherScanner.pos, ob.pos), b.pos)
					calcPositions.append(calcPos)
					
		eprint(calcPositions)
		lm = listMode(calcPositions)
		eprint(lm)

		self.pos = lm
		eprint("Scanner {} is at pos {}".format(self.scannerId, self.pos))

		
	def rotateScanner(self, rotNumber):
		#eprint("Rotating scanner {} to rot num {}".format(self.scannerId, rotNumber))
		self.beaconCoords = []
		for origBeaconCoord in self.origBeaconCoords:
			nc = applyPointRotation(origBeaconCoord, rotNumber)
			self.beaconCoords.append(nc)
			
		self.createBeaconList()
		
	def getAbsBeacondCoords(self):
		# Returns a list of the beacons with their abs coordinates
		retVal = set()
		for b in self.beaconCoords:
			retVal.add( tuple(vecAdd(self.pos, b))  )
		return retVal
		
def findAndPosNearbyScanners(knownScanners, unknownScanners):
	# Return a list of scanners that are now known
	retVal = []
	eprint("findAndPosNearbyScanners({},{})".format(len(knownScanners), len(unknownScanners)))
	
	for ks in knownScanners:
		closestScanner = ks.findClosestScanner(unknownScanners)
		
		if closestScanner == None:
			eprint("No unknown scanners near scanner {}".format(ks.scannerId))
			continue
			
		eprint("Closest scanner is : {}, rotating through {} positions".format(closestScanner.scannerId, len(transforms)))
				
		rotScores = {}
		for i in range(len(transforms)):
		#for i in range(6, 7):
		
			#eprint("Rotation *************************************************** {}".format(i))
			closestScanner.rotateScanner(i)
			#cn.dump()
			rs = ks.numberOfIdenticalBeacons(closestScanner)
			rotScores[rs] = i
			
		eprint("Rot Scores = {}".format(rotScores))
		
		bestRotSame = max([ x for x in rotScores.keys() ])
		bestRot = rotScores[bestRotSame]
		eprint("Best Rot = {}".format(bestRot))
		
		
		closestScanner.rotateScanner(bestRot)
		closestScanner.determineScannerPos(ks)
		
		retVal.append(closestScanner)
		
	return retVal
		
	

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
	
	# scanner 0 is at 0,0 by definition
	scannerList[0].pos = [0,0,0]
		
	knownScanners = []
	freshKnownScanners = [ scannerList[0] ]
	unknownScanners = scannerList[1:]

	eprint("Created {} scanners".format(len(scannerList)))
	
	while len(unknownScanners):
		eprint("Main search loop executing!")
		foundScanners = findAndPosNearbyScanners(freshKnownScanners, unknownScanners)
		
		eprint("Found scanners: {}".format(len(foundScanners)))
		
		for fs in foundScanners:
			eprint("Updating lists for scanner {}".format(fs.scannerId))
			freshKnownScanners.append(fs)
		
			for i in range(len(unknownScanners)):
				if unknownScanners[i].scannerId == fs.scannerId:
					unknownScanners.pop(i)
					break
	
	# At this point, all the scanners are rotated to same orientation
	# Should be easy to determine position for all beacons now
	completeList = set()
	
	for s in scannerList:
		absCoords = s.getAbsBeacondCoords()
		eprint("Abs beacons for scanner {} is {}".format(s.scannerId, absCoords))
		completeList = completeList.union(absCoords)
		
	eprint("Number of unique beacons: {}".format(len(completeList)))
	#eprint("List: {}".format(completeList))
	
	
	
	'''
	
	for s in scannerList:
		s.dump()
		
	#cn = scannerList[0].findClosestScanner(scannerList[1:])
	#eprint("Closest scanner is {}".format(cn.scannerId))
	
	#otherScanner = scannerList[cn]
	
	cn = scannerList[1]
	
	rotScores = {}
	for i in range(len(transforms)):
	#for i in range(6, 7):
	
		#eprint("Rotation *************************************************** {}".format(i))
		cn.rotateScanner(i)
		#cn.dump()
		rs = scannerList[0].numberOfIdenticalBeacons(cn)
		rotScores[rs] = i
		
	eprint("Rot Scores = {}".format(rotScores))
	
	bestRotSame = max([ x for x in rotScores.keys() ])
	bestRot = rotScores[bestRotSame]
	eprint("Best Rot = {}".format(bestRot))
	
	cn.rotateScanner(bestRot)
	cn.determineScannerPos(scannerList[0])
	'''
	
	
if __name__ == "__main__":
	main(sys.argv)
