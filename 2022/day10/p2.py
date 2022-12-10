#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	crt = open("crt.txt", "w")

	interestingCycles = [ 20, 60, 100, 140, 180, 220 ]
	sumIntCycles = 0

	curCycle = 0
	curIns = 0
	regX = 1

	while(curIns < len(data)):
		curCycle += 1

		beamPos = (curCycle - 1) % 40
		if beamPos == 0:
			crt.write("\n")
		if (beamPos >= (regX-1) ) and (beamPos <= (regX+1) ):
			crt.write("#")
		else:
			crt.write(".")
		
		ins = data[curIns]
		insParts = ins.split(" ")
		eprint("Cycle = {} Ins = {} RegX = {} Ins = {}".format(curCycle, curIns, regX, ins))


		if curCycle in interestingCycles:
			sumIntCycles += regX * curCycle
			eprint("*** INTERESTING CYCLE {} * {} = {} , SUM = {}".format(curCycle, regX, curCycle * regX, sumIntCycles))


		if insParts[0] == "noop":
			curIns += 1

		if insParts[0] == "addx":
			# This is a 2 cycle instruction
			data[curIns] = "addx2 " + insParts[1]

		if insParts[0] == "addx2":
			# 2nd part of 2 cycle add instrution
			regX += int(insParts[1])
			curIns += 1
	print("Sum Int Cycles = {}".format(sumIntCycles))
	crt.close()
if __name__ == "__main__":
	main(sys.argv)
