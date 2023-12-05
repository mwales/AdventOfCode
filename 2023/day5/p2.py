#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
		print(msg) 

class ConversionMap:
	def __init__(self, datalines):
		self.sourceList = []
		self.destList = []
		self.lenList = []
		self.offsetList = []

		firstLine =  datalines[0]
		sourceTypeEnd = firstLine.find("-")
		self.sourceType = firstLine[0:sourceTypeEnd]

		destTypeStart = sourceTypeEnd + 4
		destTypeEnd = firstLine.find(" ")
		self.destType = firstLine[destTypeStart:destTypeEnd]

		debug(f"Creating new convertions map for {self.sourceType} to {self.destType}")

		for singleLine in datalines[1:]:
			datalineparts = singleLine.split()
			self.destList.append( int(datalineparts[0]) )
			self.sourceList.append( int(datalineparts[1]) )
			self.lenList.append( int(datalineparts[2]) )
			self.offsetList.append( int(datalineparts[0]) - int(datalineparts[1]) )

		debug(f"  This map has {len(self.destList)} conversions")

	def getConversion(self, sourceType):
		if (sourceType == self.sourceType):
			return self.destType

	def getConversionValue(self, sourceInterval):
		debug(f"  Converting {sourceInterval}")
		offset = 0
		resultIntervals = []
		userStartVal = sourceInterval[0]
		userNumVals = sourceInterval[1]
	
		# I struggled with this algorithm for a while / had many wrong ones
		# The entire interval I get has to be mapped to something, nothing can be unmapped
		# So just start right at the beginning of what user gives you

		curValPos = userStartVal
		userNumsLeft = userNumVals
		while(userNumsLeft > 0):
			# Find the closest mapping
			closestMap = None
			for mapIndex in range(len(self.sourceList)):
				curMapStart = self.sourceList[mapIndex]
				curMapLen = self.lenList[mapIndex]
				if (curMapStart >= curValPos):
					# Map starts after current pos
					if (closestMap == None):
						closestMap = mapIndex
					elif (self.sourceList[closestMap] > curMapStart):
						closestMap = mapIndex
				else:
					# Map starts before current pos
					if (curMapStart + curMapLen > curValPos):
						# This is our map!
						closestMap = mapIndex

			debug(f"  Closest map is {closestMap}")

			if (closestMap == None):
				# We our past any existing maps
				debug(f"  No maps availabe for {curValPos},{userNumsLeft}")
				resultIntervals.append( (curValPos, userNumsLeft) )
				userNumsLeft = 0
			else:
				# Create an interval for everything before this next closest map
				closestMapStart = self.sourceList[closestMap]
				closestMapLen = self.lenList[closestMap]
				closestMapOffset = self.offsetList[closestMap]
				
				# Do we need to create a raw interval before our list?
				if (closestMapStart > curValPos):
					# Raw mapping len
					rawMapLen = closestMapStart - curValPos
					if (rawMapLen > userNumsLeft):
						debug(f"  Creating raw map before (and ending the user inteval")
						resultIntervals.append( (curValPos, userNumsLeft) )
						userNumsLeft = 0
					else:
						debug(f"  Creating raw map before, but keeps going")
						resultIntervals.append( (curValPos, rawMapLen) )
						userNumsLeft -= rawMapLen
						curValPos += rawMapLen
						# Could probably just add an extra interval for the mapped data at this point, but we can also just let loop run again
				else:
					# Use our actual mapping
					mapPointsLeft = closestMapLen - (curValPos - closestMapStart)
					if (mapPointsLeft < userNumsLeft):
						debug(f"  Using offset {closestMapOffset} till end of our map")
						resultIntervals.append( (curValPos + closestMapOffset, mapPointsLeft) )
						curValPos += mapPointsLeft
						userNumsLeft -= mapPointsLeft
					else:
						debug(f"  Using offset {closestMapOffset} till end of our user list")
						resultIntervals.append( (curValPos + closestMapOffset, userNumsLeft) )
						userNumsLeft = 0
		
		debug(f" Result intervals: {resultIntervals}")
		return resultIntervals
		

def doConversion(cmList, seedNum, numSeeds):
	curType = "seed"
	intervalValues = [ (seedNum, numSeeds) ]
	while(curType != "location"):
		for cm in cmList:
			destType = cm.getConversion(curType)
			if (destType != None):
				debug(f"We can convert {curType} to {destType}")
				curType = destType
				newIV = []
				for curIV in intervalValues:
					newIV.extend(cm.getConversionValue(curIV))
				intervalValues = newIV
				debug(f"New value after convertion is {intervalValues}")

	debug(f"Resulting intervals from doConversion:")
	debug(f"  {intervalValues}")

	minValue = intervalValues[0][0]
	for iv in intervalValues:
		if (minValue > iv[0]):
			minValue = iv[0]

	return minValue


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	seedsLine = data[0]

	listOfBlankLines = []
	for curLine in range(len(data)):
		if (data[curLine] == ""):
			listOfBlankLines.append(curLine)

	debug(f"Blank line list = {listOfBlankLines}")

	cmList = []
	for i in range(len(listOfBlankLines)):
		startLine = listOfBlankLines[i] + 1
		if ((i+1) >= len(listOfBlankLines)):
			# Last line
			cmList.append(ConversionMap(data[startLine:]))
		else:
			endLine = listOfBlankLines[i+1]
			cmList.append(ConversionMap(data[startLine:endLine]))

	seedRanges = [ int(x) for x in seedsLine.split()[1:] ]
	debug(f"Seeds: {seedRanges}")

	lowestLoc = None
	
	for i in range(0, len(seedRanges), 2):
		seedStart = seedRanges[i]
		numSeeds = seedRanges[i+1]
		curLoc = doConversion(cmList, seedStart, numSeeds)
		#debug(f"Seed {s} mapped to loc {curLoc}")
		if lowestLoc == None:
			#debug(f"Lowest location initial val {curLoc}")
			lowestLoc = curLoc
		if lowestLoc > curLoc:
			lowestLoc = curLoc
			#debug(f"Lowest location update {lowestLoc}")

	print(lowestLoc)

if __name__ == "__main__":
	main(sys.argv)
