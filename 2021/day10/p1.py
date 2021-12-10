#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def checkLine(singleLine):
	symStack = []
	startStopMap = { ')': '(', ']' : '[', '}' : '{', '>' : '<' }
	scoreTable = { ')' : 3, ']' : 57, '}' : 1197, '>' : 25137 }
	
	eprint("Start processing: {}".format(singleLine))
	
	for singleChar in singleLine:
		if singleChar in startStopMap.values():
			#eprint("Adding to stack: {}".format(singleChar))
			symStack.append(singleChar)
		else:
			if symStack.pop() != startStopMap[singleChar]:
				eprint("{} bad {}".format(singleLine, singleChar))
				return scoreTable[singleChar]
	
	eprint("{} OK".format(singleLine))
	return 0

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	solution = 0
	for singleLine in filedata:
		solution += checkLine(singleLine)
		
	print("Sol = {}".format(solution))

if __name__ == "__main__":
	main(sys.argv)
