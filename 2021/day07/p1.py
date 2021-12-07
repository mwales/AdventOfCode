#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def crabDistance(crabs, dest):
	retVal = 0
	for c in crabs:
		retVal += abs(c - dest)
	return retVal

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	crabs = [ int(x) for x in filedata[0].split(",") ]
	
	
	minCrab = min(crabs)
	maxCrab = max(crabs)
	
	solves = {}
	for i in range(minCrab, maxCrab - 1):
		solves[i] = crabDistance(crabs, i)
		
	minSolve = min(solves.values())
	for i in solves:
		if (solves[i] == minSolve):
			print("Dist i = {} = {}".format(i, minSolve))
			

if __name__ == "__main__":
	main(sys.argv)
