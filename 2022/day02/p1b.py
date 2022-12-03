#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def scoreGame(opp, me):
	outcomeMap = { "rock"    : { "rock": 3, "paper": 6, "scissor": 0 },
	               "paper"   : { "rock": 0, "paper": 3, "scissor": 6 },
	               "scissor" : { "rock": 6, "paper": 0, "scissor": 3 } }
	
	outcome = outcomeMap[opp][me]

	scoreMeMap = { 'rock': 1, 'paper': 2, 'scissor': 3 }

	retVal = outcome + scoreMeMap[me]
	eprint("{} + {} = {}".format(outcome, scoreMeMap[me], retVal))
	return retVal

def mapOppChoice(opp):
	gameMap = { 'A': "rock", 'B': "paper", 'C': "scissor" }
	return gameMap[opp]

def mapMe(me):
	gameMap = { 'X': "rock", 'Y': "paper", 'Z': "scissor" }
	return gameMap[me]

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
		o = mapOppChoice(opponent)
		m = mapMe(me)
		eprint("opp = {}  and me = {}".format(o, m))

		scoreTotal += scoreGame(o, m)

	print("Total Score = {}".format(scoreTotal))

if __name__ == "__main__":
	main(sys.argv)
