#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
		print(msg + "\n")

spelledOutDigits = { "one": 1,
                     "two": 2,
                     "three": 3,
                     "four": 4,
                     "five": 5,
                     "six": 6,
                     "seven": 7,
                     "eight": 8,
                     "nine": 9 }


def getFirstDigit(msg):
	firstDigitPos = len(msg)

	for it in spelledOutDigits:
		curPos = msg.find(it)
		if (curPos >= 0):
			if (curPos < firstDigitPos):
				firstDigitPos = curPos
				retVal = spelledOutDigits[it]

	for i in range(10):
		curPos = msg.find(str(i))
		if (curPos >= 0):
			if (curPos < firstDigitPos):
				firstDigitPos = curPos
				retVal = int(msg[curPos])

	
	return retVal


def getLastDigit(msg):
	firstDigitPos = -1

	for it in spelledOutDigits:
		curPos = msg.rfind(it)
		debug(f"Searching for {it} in {msg} ret {curPos}")
		if (curPos >= 0):
			if (curPos > firstDigitPos):
				firstDigitPos = curPos
				retVal = spelledOutDigits[it]

	for i in range(10):
		curPos = msg.rfind(str(i))
		debug(f"Searching for {i} in {str} ret {curPos}")
		if (curPos >= 0):
			if (curPos > firstDigitPos):
				firstDigitPos = curPos
				retVal = int(msg[curPos])

	return retVal



def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	sum = 0
	for sl in data:
		firstNumPos = getFirstDigit(sl)
		lastNumPos = getLastDigit(sl)

		
		debug(f"First = {firstNumPos} and second = {lastNumPos}")

		sum += firstNumPos * 10 + lastNumPos

	print(sum)

if __name__ == "__main__":
	main(sys.argv)
