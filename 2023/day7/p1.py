#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg)

card_map = { 'A': 14,
             'K': 13,
             'Q': 12,
             'J': 11,
             'T': 10,
             '9': 9,
             '8': 8,
             '7': 7,
             '6': 6,
             '5': 5,
             '4': 4,
             '3': 3,
             '2': 2 }

class CardHand:
	def __init__(self, cardLetters):
		self.hand = cardLetters

	def getCardFreqs(self):
		retVal = {}
		for sc in self.hand:
			curFreq = retVal.get(sc, 0)
			curFreq += 1
			retVal[sc] = curFreq

		return retVal

	def __repr__(self):
		return self.hand

	def isXOfAKind(self, howMany):
		fd = self.getCardFreqs()
		for curFreq in fd:
			if fd[curFreq] == howMany:
				return True
		return False

	def isFullHouse(self):
		fd = self.getCardFreqs()
		if (len(fd) != 2):
			return False

		if (fd[self.hand[0]] == 2) or (fd[self.hand[0]] == 3):
			return True
		return False

	def isTwoPair(self):
		numPairs = 0
		fd = self.getCardFreqs()
		for curFreq in fd:
			if fd[curFreq] == 2:
				numPairs += 1

		return numPairs == 2

	def compareCardString(self, cardString1, cardString2):
		if (cardString1 == cardString2):
			debug(f"compareCardString({cardString1}, {cardString2}) is equal")
			return 0

		for i in range(len(cardString1)):
			curCard1 = cardString1[i]
			curCard2 = cardString2[i]
			curVal1 = card_map[curCard1]
			curVal2 = card_map[curCard2]
			if (curVal1 < curVal2):
				debug(f"compareCardString({cardString1}, {cardString2}) 1 < 2")
				return -1
			elif (curVal1 > curVal2):
				debug(f"compareCardString({cardString1}, {cardString2}) 1 > 2")
				return 1

		debug(f"compareCardString({cardString1}, {cardString2}) broken")
		return 0

	def getHandRank(self):
		rank = '2'
		rankStr = "High Card"
		if self.isXOfAKind(2):
			rank = '3'
			rankStr = "Pair"
		if self.isTwoPair():
			rank = '4'
			rankStr = "TwoPair"
		if self.isXOfAKind(3):
			rank = '5'
			rankStr = "Three of a Kind"
		if self.isFullHouse():
			rank='6'
			rankStr = "Full House"
		if self.isXOfAKind(4):
			rank = '7'
			rankStr = "Four of a Kind"
		if self.isXOfAKind(5):
			rank = '8'
			rankStr = "Five of a Kind"
		debug(f"getHandRank of {self.hand} is {rank} = {rankStr}")
		return rank

	def compareHand(self, otherHand):
		selfRank = self.getHandRank()
		otherRank = otherHand.getHandRank()

		selfRankedCardString = selfRank + self.hand
		otherRankedCardString = otherRank + otherHand.hand

		return self.compareCardString(selfRankedCardString, otherRankedCardString)

	def getHandValue(self):
		retValStr = self.getHandRank() # always less than 0xa

		for eachCard in self.hand:
			retValStr += hex(card_map[eachCard])[-1:]

		return int(retValStr, 16)

def scoreHand(hand):
	return hand.getHandValue()

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	handData = []
	betData = {}
	for singleLine in data:
		lineParts = singleLine.split()
		curHand = CardHand(lineParts[0])
		bet = int(lineParts[1])
		handData.append(curHand)
		betData[curHand] = bet

		curRank = curHand.getHandRank()
		curValue = curHand.getHandValue()
		debug(f"For {curHand} the rank is {curRank} and value is {hex(curValue)}")

	debug(f"All Game Data: {handData}")

	debug(f"Freq test: f{handData[0].getCardFreqs()}")

	handData.sort(key=scoreHand)

	winnings = 0
	multiplier = 1
	for hand in handData:
		winnings += multiplier * betData[hand]
		multiplier += 1
	
	print(f"Winnings: {winnings}")


if __name__ == "__main__":
	main(sys.argv)
