#!/usr/bin/env python3

import sys, math

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
	keepRunning = True

	ghostState = []
	for singleNode in bigMap:
		if singleNode[-1] == 'A':
			ghostState.append(bigMap[singleNode])

	numGhosts = len(ghostState)
	debug(f"Number of ghosts = {numGhosts}")
	debug(f"{ghostState}")

	goalTimes = []
	for sg in ghostState:
		initialGoal = None
		secondGoal = None
		stepCounter = 0
		
		while secondGoal == None:
			for eachturn in directions:
				stepCounter += 1
				if eachturn == "L":
					nn = sg.left
					sg = bigMap[nn]
					debug(f"Step {stepCounter} brings ghost to {nn}")
				else:
					nn = sg.right
					sg = bigMap[nn]
					debug(f"Step {stepCounter} brings ghost to {nn}")

				if sg.name[-1] == 'Z':
					if (initialGoal == None):
						initialGoal = stepCounter
						debug(f"Ghost reached goal first time in {stepCounter} steps")
						stepCounter = 0
					else:
						secondGoal = stepCounter
						debug(f"Ghost reached goal second time in {stepCounter} more steps")
						break
		goalTimes.append( (initialGoal, secondGoal) )

	debug(f"All Goal Times: {goalTimes}")

	simpleTimes = []
	for gt in goalTimes:
		if gt[0] != gt[1]:
			print("Ah crap, this won't work")
		else:
			simpleTimes.append(gt[0])

	finalCount = math.lcm(*simpleTimes)

	print(finalCount)


if __name__ == "__main__":
	main(sys.argv)
