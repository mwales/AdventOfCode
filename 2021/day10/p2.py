#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def scoreBadCharacter(badchar):
	scoreTable = { ')' : 3, ']' : 57, '}' : 1197, '>' : 25137 }
	return scoreTable[badchar]

def scoreTermCharacter(badchar):
	scoreTable = { '(' : 1, '[' : 2, '{' : 3, '<' : 4 }
	return scoreTable[badchar]
	
def checkLine(singleLine):
	symStack = []
	startChar = [ '(', '[', '{', '<' ]
	stopChar = [ ')', ']', '}', '>' ]
	
	
	eprint("Start processing: {}".format(singleLine))
	
	for singleChar in singleLine:
		if singleChar in startChar:
			eprint("Adding to stack: {}".format(singleChar))
			symStack.append(singleChar)
		else:
			if symStack.pop() == startChar[stopChar.index(singleChar)]:
				eprint("Remvoing from stack: {}".format(singleChar))

			else:
				eprint("{} bad {}".format(singleLine, singleChar))
				return 0
	
	eprint("{} OK".format(singleLine))
	
	# Finish the line
	eprint("symStack = {}".format(symStack))
	
	score = 0
	while len(symStack) > 0:
		termChar = symStack.pop()
		score *= 5
		score += scoreTermCharacter(termChar)
		eprint("Score after loop = {}".format(score))
		
	
		
	eprint("Score = {}".format(score))
	return score
		

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	scoreList = []
	for singleLine in filedata:
		s = checkLine(singleLine)
		if s != 0:
			scoreList.append(checkLine(singleLine))
		
	scoreList.sort()
	eprint("ScoreList = {}".format(scoreList))
	
	score = scoreList[len(scoreList) // 2]
	print("Sol = {}".format(score))
			

if __name__ == "__main__":
	main(sys.argv)
