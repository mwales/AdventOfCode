#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
class BingoCard:
	def __init__(self, cardNumberStrings):
		
		self.cardSize = len(cardNumberStrings)
		
		self.cardNumbers = {}
		self.markedSquares = set()
		
		for row in range(0, self.cardSize):			
			rowVals = [int(x) for x in cardNumberStrings[row].split()]
			for col in range(0, self.cardSize):			
				self.cardNumbers[(col,row)] = rowVals[col]
		
	def getValue(self, x, y):
		return self.cardNumbers[(x,y)]
		
	def isMarked(self, x, y):
		return (x,y) in self.markedSquares
	
	def markCard(self, value):
		for loc in self.cardNumbers:
			if (self.cardNumbers[loc] == value):
				self.markedSquares.add(loc)
		
	def printCard(self):
		for y in range(0, self.cardSize):
			rowText = ""
			for x in range(0, self.cardSize):
				if self.isMarked(x, y):
					rowText += "X%2dX " % self.getValue(x, y)
				else:
					rowText += " %2d  " % self.getValue(x, y)
			eprint(rowText)
	
	def isWinner(self):
		#eprint("isWinner on : {}".format(self.markedSquares))
		winningData = 'X' * self.cardSize		
		
		#eprint("Winning Data: {}".format(winningData))
		
		# Check all rows
		for eachRow in range(self.cardSize):
			numMarked = 0
			for eachCol in range(self.cardSize):
				if self.isMarked(eachCol, eachRow):
					numMarked += 1
			if (numMarked == self.cardSize):
				return True
		
		# Check all cols
		for eachCol in range(self.cardSize):
			numMarked = 0
			for eachRow in range(self.cardSize):
				if self.isMarked(eachCol, eachRow):
					numMarked += 1
			if (numMarked == self.cardSize):
				return True
		
		return False
		
	def sumOfAllUnmarked(self):
		retData = 0
		for y in range(self.cardSize):
			for x in range(self.cardSize):
				if not self.isMarked(x,y):
					retData += self.getValue(x,y)
		return retData
		

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	gameData = f.read().strip().split("\n")
	f.close()
	
	calledNumberStrings = gameData[0].split(',')
	calledNumbers = [ int(x) for x in calledNumberStrings ]
	
	#eprint("Called Numbers: {}".format(calledNumbers))
	
	# Create all the bingo cards
	bingoCards = []
	curCard = []
	for i in range(2, len(gameData)):
		if (gameData[i] == ""):
			# End of a card
			bingoCards.append(BingoCard(curCard))
			curCard = []
		else:
			curCard.append(gameData[i])
	
	if (len(curCard) != 0):
		bingoCards.append(BingoCard(curCard))
	
	winningCard = None
	winningValue = None
	for curCalledNum in calledNumbers:
		
		for eachCard in bingoCards:
			eachCard.markCard(curCalledNum)
			
		cardsToRemove = []
		for eachCard in bingoCards:
			if eachCard.isWinner():
				cardsToRemove.append(eachCard)
		
		for deadCard in cardsToRemove:
			bingoCards.remove(deadCard)
			
		if (len(bingoCards) == 0):
			eprint("Found the last winner")
			
			score = curCalledNum * cardsToRemove[0].sumOfAllUnmarked()
			print("Score of last winning card: {}".format(score))
			return
				

		'''
		eprint("After {} was called out".format(curCalledNum))		
		for eachCard in bingoCards:
			eprint("Card Data:")
			eachCard.printCard()
			eprint("")
		'''

		

if __name__ == "__main__":
	main(sys.argv)
