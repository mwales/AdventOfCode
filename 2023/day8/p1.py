#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

class MapNode:
	def __init__(self, text):
		text = text.replace("(","")
		text = text.replace(")","")
		text = text.replace("=","")
		text = text.replace(",","")
		parts = text.split()
		debug(parts)

		self.name = parts[0]
		self.left = parts[1]
		self.right = parts[2]

	def __repr__(self):
		return f"{self.name} L={self.left} R={self.right}"

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	directions = data[0]

	mapData = data[2:]
	bigMap = {}
	for eachLine in mapData:
		mn = MapNode(eachLine)
		bigMap[mn.name] = mn

	debug(bigMap)

	stepCounter = 0
	curNode = bigMap['AAA']
	keepRunning = True
	while keepRunning:
		for eachturn in directions:
			stepCounter += 1
			if eachturn == "L":
				nn = curNode.left
			else:
				nn = curNode.right

			debug(f"Step {stepCounter} takes us to {nn}")
			curNode = bigMap[nn]

			if curNode.name == 'ZZZ':
				keepRunning = False
				break
	
	print(f"Num steps = {stepCounter}")

if __name__ == "__main__":
	main(sys.argv)
