#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

blinkingCache = dict()

def blinkSingleStone(stone, numBlinks):
	if (numBlinks == 0):
		# recursion end
		return 1

	if ( (stone,numBlinks) in blinkingCache ):
		return blinkingCache[(stone, numBlinks)]

	if (stone == 0):
		newStone = 1
		retVal = blinkSingleStone(newStone, numBlinks - 1)
		blinkingCache[(stone, numBlinks)] = retVal
		return retVal

	strStone = str(stone)
	strStoneLen = len(strStone)

	if (strStoneLen % 2) == 0:
		# even number of digits
		stones = []
		stones.append(int(strStone[:strStoneLen//2]))
		stones.append(int(strStone[strStoneLen//2:]))
		retVal = blinkMultipleStones(stones, numBlinks - 1)
		blinkingCache[(stone, numBlinks)] = retVal
		return retVal
	else:
		newStone = stone * 2024
		retVal = blinkSingleStone(newStone, numBlinks - 1)
		blinkingCache[(stone, numBlinks)] = retVal
		return retVal


def blinkMultipleStones(stones, numBlinks):
	if (numBlinks == 0):
		return len(stones)
	
	retVal = 0
	for s in stones:
		retVal += blinkSingleStone(s, numBlinks)

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

	numStones = blinkMultipleStones(stones,25)

	#print(f"Stones: {stones}")

	print(f"Part 1 = {numStones}")

	numStones = blinkMultipleStones(stones,75)
	
	print(f"Part 2 = {numStones}")

if __name__ == "__main__":
	main(sys.argv)
