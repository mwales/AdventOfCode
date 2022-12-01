#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	calData = f.read().strip().split("\n")
	f.close()

	elfCalList = []

	curCalTotal = 0
	for eachLine in calData:
		if eachLine == "":
			elfCalList.append(curCalTotal)
			curCalTotal = 0
		else:
			curCalTotal += int(eachLine)
	elfCalList.append(curCalTotal)

		
	maxId = -1
	curMax = 0
	for i in range(0, len(elfCalList)):
		eprint("{} = {}".format(i, elfCalList[i]))
		
		if elfCalList[i] >= curMax:
			maxId = i
			curMax = elfCalList[i]
			eprint("new max = ", i)
		
	print("Elf = ", maxId, " with ", curMax)

	elfCalList.sort(reverse=True)
	eprint(elfCalList)

	eprint("3 top elfs = {}".format(elfCalList[0] + elfCalList[1] + elfCalList[2]))

if __name__ == "__main__":
	main(sys.argv)
