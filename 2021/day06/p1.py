#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	initData = [ int(x) for x in filedata[0].split(",") ]
	
	# Initialize population tracker
	poptracker = {}
	for i in range(0, 9):
		poptracker[i] = 0
	for eachFish in initData:
		poptracker[eachFish] += 1
		
	eprint("Init : {}".format(poptracker))
		
	nextiter = poptracker
	for day in range(80):
		newyoots = poptracker[0]
		
		for i in range(9):
			if (i == 6):
				eprint("i = {}, poptracker[i+1] = {}, newyoots = {}".format(i, poptracker[i+1], newyoots))
				poptracker[i] = poptracker[i+1] + newyoots
				eprint("poptracker[i] = {}".format(poptracker[i]))
			elif (i == 8):
				poptracker[i] = newyoots
			else:
				poptracker[i] = poptracker[i+1]
		
		eprint("Day {}: {}".format(day + 1, nextiter))
		
		
	sumOfAll = 0
	for eachPop in poptracker:
		sumOfAll += poptracker[eachPop]
		
	print("Sum = {}".format(sumOfAll))

if __name__ == "__main__":
	main(sys.argv)
