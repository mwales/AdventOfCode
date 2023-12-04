#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

def playCard(card):
	cardIdParts = card.split(":")

	cardId = int(cardIdParts[0][cardIdParts[0].find(" "):])
	cardIdJustId = cardIdParts[0].split(" ")
	#cardId = int(cardIdJustId[1])
	debug(f"Playing card id {cardId}")

	numberParts = cardIdParts[1].split("|")

	winningNums = set()
	for x in  numberParts[0].split():
		winningNums.add(int(x))

	guessNums = set()
	for x in numberParts[1].split():
		guessNums.add(int(x))


	debug(f"  Win Nus: {winningNums}")
	debug(f"  Guess Nums: {guessNums}")

	score = 0
	for x in guessNums:
		if x in winningNums:
			debug(f"  {x} is a winner, score before = {score}")
			if (score == 0):
				score = 1
			else:
				score *= 2
	debug(f"  Score for card = {score}")
	return score


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	sumPoints = 0
	for card in data:
		sumPoints += playCard(card)

	print(sumPoints)

if __name__ == "__main__":
	main(sys.argv)
