#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def createStack(stackNum, data, stackBottom):
	curX = 1 + (stackNum * 4)
	curStack = []
	for i in range(stackBottom + 1):
		curY = stackBottom - i
		#eprint("Stack = {}, curX = {}, curY = {}".format(stackNum, curX, curY))
		if (curX > len(data[curY])):
			#eprint("string length causeing stack create return")
			# No item in this stack position
			return curStack
		if (data[curY][curX] == ' '):
			# No item in this stack
			#eprint("blank pos found in stack")
			return curStack
		curStack.append(data[curY][curX])
	return curStack

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().split("\n")
	f.close()

	# which line is blank
	blankLine = -1
	for i in range(len(data)):
		if (data[i] == ""):
			blankLine = i
			break

	eprint("Blank @ {}".format(blankLine))

	# determine number of cols
	colNums = [ int(x) for x in data[blankLine - 1].split() ]
	eprint("cols = {}".format(colNums))
	maxCol = max(colNums)
	eprint("Max = {}".format(maxCol))

	# create stacks
	cs = []
	for i in range(maxCol):
		curS = createStack(i, data, blankLine - 2)
		eprint("stack {} = {}".format(i, curS))
		cs.append(curS)

	eprint("Data:")
	eprint(data[:blankLine])

	eprint("Stacks:")
	eprint(cs)

	for i in range(blankLine + 1, len(data), 1):
		if (data[i] == ""):
			continue
		eprint("Process {}".format(data[i]))

		movParts = data[i].split(" ")
		eprint("movParts = {}".format(movParts))

		qty = int(movParts[1])
		fromS = int(movParts[3])
		toS = int(movParts[5])

		crates = cs[fromS-1][-qty:]
		cs[fromS-1] = cs[fromS-1][:-qty]
		eprint("Moving crates {} from {} to {}".format(crates, fromS, toS))
		for c in crates:
			cs[toS-1].append(c)

		eprint(cs)

	solve = ""
	for s in cs:
		solve += s[-1]

	print("Solution p1 = {}".format(solve))



if __name__ == "__main__":
	main(sys.argv)
