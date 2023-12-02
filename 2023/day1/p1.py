#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
		print(msg + "\n")

def getFirstDigit(msg):
	for i in msg:
		if ( i >= '0') and (i <= '9'):
			return int(i)
	return -1

def getLastDigit(msg):
	for i in range(len(msg)):
		curChar = msg[-(i+1)]
		if ( (curChar >= '0') and (curChar <= '9') ):
			return int(curChar)
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
