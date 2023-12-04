#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

def playCardInDeck(cardStack, cardCounts, cardId):
	debug(f"Playing card {cardId} in deck")
	scoreOfThisCard = playCard(cardStack[cardId])

	for x in range(scoreOfThisCard):
		cardCounts[cardId + x + 1] += cardCounts[cardId]

	



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
			score += 1 
	debug(f"  Score for card = {score}")
	return score


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	cardCounts = []
	for x in range(len(data)):
		cardCounts.append(1)

	debug(f"Cards: {cardCounts}")
	debug(f"Total Cards Before: {sum(cardCounts)}")

	for cardId in range(len(data)):
		debug(f"  Before Cards: {cardCounts}")
		playCardInDeck(data, cardCounts, cardId)
		debug(f"  After Cards: {cardCounts}")

	debug(f"Cards: {cardCounts}")
	debug(f"Total Cards After: {sum(cardCounts)}")
	#print(sumPoints)

if __name__ == "__main__":
	main(sys.argv)
