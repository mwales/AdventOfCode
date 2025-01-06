#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		#sys.stderr.write(f"{msg}\n")
		print(msg)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	ll = []
	rl = []
	for line in data:
		li = int(line.split()[0])
		ri = int(line.split()[1])
		ll.append(li)
		rl.append(ri)

	ll.sort()
	rl.sort()

	distCum = 0
	for i in range(len(ll)):
		dist = abs(ll[i] - rl[i])
		distCum += dist
		#print(f"dist = {dist} and distCum = {distCum}")

	simCum = 0
	print(f"Part 1 = {distCum}")

	for i in range(len(ll)):
		curSimScore = 0
		for j in range(len(rl)):
			if ll[i] == rl[j]:
				curSimScore += 1
		curSimScore *= ll[i]
		simCum += curSimScore

	print(f"Part 2 = {simCum}")


if __name__ == "__main__":
	main(sys.argv)
