#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def blink(stones):
	retVal = []
	for s in stones:
		strStone = str(s)
		strStoneLen = len(strStone)
		if s == 0:
			retVal.append(1)
		elif (strStoneLen % 2) == 0:
			retVal.append(int(strStone[:strStoneLen//2]))
			retVal.append(int(strStone[strStoneLen//2:]))
		else:
			retVal.append(s*2024)
	return retVal
			

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	stones = data[0].split()
	stones = [ int(x) for x in stones ]

	print(f"Stones: {stones}")

	for i in range(25):
		stones = blink(stones)

		#print(f"Stones: {stones}")

	print(f"Part 1 = {len(stones)}")

	for i in range(50):
		stones = blink(stones)

	print(f"Part 2 = {len(stones)}")

if __name__ == "__main__":
	main(sys.argv)
