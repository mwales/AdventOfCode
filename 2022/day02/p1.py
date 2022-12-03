#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def scoreGame(opp, me):
	if (opp == 'A'):
		# opp is rock
		if (me == 'X'):
			outcome = 3
		elif (me == 'Y'):
			outcome = 6
		else:
			outcome = 0
	elif (opp == 'B'):
		# opp is paper
		if (me == 'X'):
			outcome = 0
		elif (me == 'Y'):
			outcome = 3
		else:
			outcome = 6
	else:
		# opp is scissors
		if (me == 'X'):
			outcome = 6
		elif (me == 'Y'):
			outcome = 0
		else:
			outcome = 3

	scoreMeMap = { 'X': 1, 'Y': 2, 'Z': 3 }

	retVal = outcome + scoreMeMap[me]
	eprint("{} + {} = {}".format(outcome, scoreMeMap[me], retVal))
	return retVal

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	scoreTotal = 0
	for eachGame in data:
		opponent, me = eachGame.split(" ")

		eprint("opp = {}  and me = {}".format(opponent, me))

		scoreTotal += scoreGame(opponent, me)

	print("Total Score = {}".format(scoreTotal))

if __name__ == "__main__":
	main(sys.argv)
