#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

def solveRace(rt, dist):
	debug(f"Race of time {rt} and {dist}")
	wins = 0
	for i in range(rt):
		curDist = (rt - i) * i
		debug(f"  Hold {i} secs gets {curDist}")
		if (curDist > dist):
			wins += 1
	
	debug(f"Wins = {wins}")
	return wins

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	times = [ int(x) for x in data[0].split()[1:] ]
	distances = [ int(x) for x in data[1].split()[1:] ]

	result = None
	for i in range(len(times)):
		curRes = solveRace(times[i], distances[i])
		if (result == None):
			result = curRes
		else:
			result *= curRes
	
	print(result)

if __name__ == "__main__":
	main(sys.argv)
