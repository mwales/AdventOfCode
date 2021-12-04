#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
class BingoCard:
	def __init__(self, cardNumberStrings):
		
		self.cardSize = len(cardNumberStrings)
		
		
		
		self.cardNumbers = []
		self.markedSquares = []
		
		for row in range(0, self.cardSize):
			markedRowData = []			
			for col in range(0, self.cardSize):
				markedRowData.append('.')
			self.markedSquares.append(markedRowData)
			
			self.cardNumbers.append([int(x) for x in cardNumberStrings[row].split()])
		
	def getValue(self, x, y):
		return self.cardNumbers[y][x]
		
	def isMarked(self, x, y):
		if (self.markedSquares[y][x] == '.'):
			return False
		else:
			return True
	
	def markCard(self, value):
		for x in range(0, self.cardSize):
			for y in range(0, self.cardSize):
				if (self.getValue(x, y) == value):
					self.markedSquares[y][x] = 'X'
					return
		
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
		eprint("isWinner on : {}".format(self.markedSquares))
		winningData = 'X' * self.cardSize
		
		
		eprint("Winning Data: {}".format(winningData))
		
		# Check all rows
		for eachRow in self.markedSquares:
			if (''.join(eachRow) == winningData):
				return True
		
		# Check all cols
		colData = ''
		for col in range(0, self.cardSize):
			colData = ''
			for row in range(0, self.cardSize):
				colData += self.markedSquares[row][col]
			if (''.join(colData) == winningData):
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
	
	eprint("Called Numbers: {}".format(calledNumbers))
	
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
		
	eprint("Initial state:")
	for eachCard in bingoCards:
		eprint("Card Data:")
		eachCard.printCard()
		eprint("")
	
	winningCard = None
	winningValue = None
	for curCalledNum in calledNumbers:
		
		for eachCard in bingoCards:
			eachCard.markCard(curCalledNum)
			
			if eachCard.isWinner():
				gameOver = True
				print("We found the winning card!")
				eachCard.printCard()
				
				score = eachCard.sumOfAllUnmarked() * curCalledNum
				print("Score = {}".format(score))
		
				return
				

				
		eprint("After {} was called out".format(curCalledNum))
		
		for eachCard in bingoCards:
			eprint("Card Data:")
			eachCard.printCard()
			eprint("")
			

		

if __name__ == "__main__":
	main(sys.argv)
