#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

def solveSeq(numSeq):
	# Is sequence all zeros?
	allZeros = True
	for sn in numSeq:
		if (sn != 0):
			allZeros = False
			break
	
	if allZeros:
		return 0

	# If we get to this point, we are not at the end stage.  Find
	# all the differences and then call ourselves
	childSeq = []
	for i in range(len(numSeq) - 1):
		childSeq.append(numSeq[i+1] - numSeq[i])
	
	addToMe = solveSeq(childSeq)

	return numSeq[-1] + addToMe

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	sumSolution = 0
	for eachSeq in data:
		numSeq = [ int(x) for x in eachSeq.split() ]
		sumSolution += solveSeq(numSeq)

	print(sumSolution)
if __name__ == "__main__":
	main(sys.argv)
