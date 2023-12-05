#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
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

	def getConversionValue(self, sourceVal):
		offset = 0
		for i in range(len(self.destList)):
			if ( (sourceVal >= self.sourceList[i]) and (sourceVal < self.sourceList[i] + self.lenList[i]) ):
				offset = self.offsetList[i]
				debug(f"Found offset {offset} at pos {i} in list")

		return sourceVal + offset

def doConversion(cmList, seedNum):
	curType = "seed"
	curVal = seedNum
	while(curType != "location"):
		for cm in cmList:
			destType = cm.getConversion(curType)
			if (destType != None):
				debug(f"We can convert {curType} to {destType}")
				curType = destType
				curVal = cm.getConversionValue(curVal)
				debug(f"New value after convertion is {curVal}")
	return curVal


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

	seeds = [ int(x) for x in seedsLine.split()[1:] ]
	debug(f"Seeds: {seeds}")

	lowestLoc = None
	for s in seeds:
		curLoc = doConversion(cmList, s)
		debug(f"Seed {s} mapped to loc {curLoc}")
		if lowestLoc == None:
			debug(f"Lowest location initial val {curLoc}")
			lowestLoc = curLoc
		if lowestLoc > curLoc:
			lowestLoc = curLoc
			debug(f"Lowest location update {lowestLoc}")

	print(lowestLoc)

if __name__ == "__main__":
	main(sys.argv)
