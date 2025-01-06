#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def isIncreasing(levelData):
	for i in range(1,len(levelData)):
		if levelData[i-1] >= levelData[i]:
			return False
	return True

def isDecreasing(levelData):
	for i in range(1,len(levelData)):
		if levelData[i-1] <= levelData[i]:
			return False
	return True

def isCloseEnough(levelData):
	for i in range(1,len(levelData)):
		diffLevel = abs(levelData[i-1] - levelData[i])
		if (diffLevel < 1) or (diffLevel > 3):
			return False
	return True




def isSafeReport(levelData):
	if (not isIncreasing(levelData)) and (not isDecreasing(levelData)):
		debug("Not increasing or decreasing")
		return False

	if (isCloseEnough(levelData)):
		return True
	else:
		debug("Not close enough")
		return False
	

def isSafeReportPart2(levelData):
	listsOfReports = []
	listsOfReports.append(levelData)
	for i in range(len(levelData)):
		levelCopy = levelData[:]
		levelCopy.pop(i)
		listsOfReports.append(levelCopy)

	for singleReport in listsOfReports:
		if isSafeReport(singleReport):
			return True
	
	return False

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	numSafe = 0
	for report in data:
		levelData = [ int(x) for x in report.split() ]
		print(levelData)

		if isSafeReport(levelData):
			numSafe += 1

	print(f"Num safe = {numSafe}")

	numSafe2 = 0
	for report in data:
		levelData = [ int(x) for x in report.split() ]

		if isSafeReportPart2(levelData):
			numSafe2 += 1

	print(f"Num safe2 = {numSafe2}")


if __name__ == "__main__":
	main(sys.argv)
