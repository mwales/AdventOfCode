#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg + "\n")

def addAllCubes(msgData):
	retVal = { "red": 0,
	           "blue": 0,
	           "green": 0 }

	parts = msgData.split(":")
	goodParts = parts[1]
	
	hands = goodParts.split(";")
	for curHand in hands:
		debug(f"curHand = {curHand}")
		handParts = curHand.split(" ")[1:]

		for i in range(0, len(handParts), 2):
			debug(f"handParts = {handParts}")
			#debug(f"Count = {goodParts[i]} = {goodParts[i+1]}")
			count = int(handParts[i])
			color = handParts[i+1].replace(",","")

			for curColor in retVal:
				if (color == curColor) and (retVal[curColor] < count):
					retVal[curColor] =count

	return retVal

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	bagLimits = { "red": 12,
	              "green": 13,
	              "blue": 14 }

	gameSum = 0
	for i in range(len(data)):
		gameId = i + 1
		retDict = addAllCubes(data[i])
		debug(f"REsult = {retDict}")

		badGame = False
		for colorSelect in bagLimits:
			if (retDict[colorSelect] > bagLimits[colorSelect]):
				debug(f"Game{gameId} no work")
				badGame = True

		if (badGame):
			continue

		debug(f"Game {gameId} works!")
		gameSum += gameId

	print(f"{gameSum}")

if __name__ == "__main__":
	main(sys.argv)
