#!/usr/bin/env python3

import sys


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()

	p1Pos = int(stringData[0].split(" ")[-1]) - 1
	p2Pos = int(stringData[1].split(" ")[-1]) - 1

	eprint("p1 = {} and p2 = {}".format(p1Pos, p2Pos))

	p1Score = 0
	p2Score = 0

	curDie = 0
	turn = 1
	numRolls = 0

	while( (p1Score < 1000) and (p2Score < 1000) ):
		eprint("p1Pos = {}  and p2Pos = {}".format(p1Pos, p2Pos))

		die1 = curDie + 1
		curDie = (curDie + 1) % 1000
		die2 = curDie + 1
		curDie = (curDie + 1) % 1000
		die3 = curDie + 1
		curDie = (curDie + 1) % 1000

		curDieRoll = die1 + die2 + die3
		eprint("Player {} rolles {} {} {}".format(turn, die1, die2, die3))
		numRolls += 3

		if turn == 1:
			p1Pos = (p1Pos + curDieRoll) % 10
			p1Score += p1Pos + 1
			turn = 2
		else:
			p2Pos = (p2Pos + curDieRoll) % 10
			p2Score += p2Pos + 1
			turn = 1

		eprint("p1 = {}\tp2 = {}".format(p1Score, p2Score))
		eprint("Num rolls = {}".format(numRolls))

		if (p1Score > p2Score):
			loser = p2Score
		else:
			loser = p1Score

		print("Solve = {} x {} = {}".format(loser, numRolls, loser * numRolls))

if __name__ == "__main__":
	main(sys.argv)
