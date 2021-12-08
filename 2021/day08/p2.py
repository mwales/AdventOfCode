#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def wordToSet(data):
	retVal = set()
	for eachChar in data:
		retVal.add(eachChar)
	return retVal

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	solution = 0
	for singleLine in filedata:
		alldigitstogether, valuedisplay = singleLine.split('|')
		
		# a dictionary mapping known digits -> sets of segments that are on
		key = {}
		
		# setdigits is the list of sets i haven't decoded yet
		unknownDigits = [ wordToSet(x) for x in alldigitstogether.strip().split() ]
		
		# sets in the final value display that i have to decode
		setvaluedisplay = [ wordToSet(x) for x in valuedisplay.strip().split() ]
		
		eprint("number unknown = {}, unknownDigits = {}".format(len(unknownDigits), unknownDigits))
		
		# same idea as part 1, can determine which digits for 1, 4, 7, and 8
		for eachDigit in unknownDigits:
			dl = len(eachDigit)
			if (dl == 2):
				key[1] = eachDigit
			elif (dl == 4):
				key[4] = eachDigit
			elif (dl == 3):
				key[7] = eachDigit
			elif (dl == 7):
				key[8] = eachDigit
				
		unknownDigits.remove(key[1])
		unknownDigits.remove(key[4])
		unknownDigits.remove(key[7])
		unknownDigits.remove(key[8])
		
		eprint("number unknown = {}, unknownDigits = {}".format(len(unknownDigits), unknownDigits))
		eprint("Key = {}".format(key))
		
		# Figure out 3 and 6
		for curDigit in unknownDigits:
			dl = len(curDigit)
			if (dl == 5):
				if key[1].issubset(curDigit):
					# Both 1 segments are in 3, but aren't in 5 or 2
					key[3] = curDigit
			if (dl == 6):
				if not key[1].issubset(curDigit):
					# 6 digit doesn't contain both the 1 segments (cc and ff), 9 and 0 do
					key[6] = curDigit
					
		eprint("3 = {}".format(key[3]))
		eprint("6 = {}".format(key[6]))
		
		unknownDigits.remove(key[3])
		unknownDigits.remove(key[6])
		
		eprint("number unknown = {}, unknownDigits = {}".format(len(unknownDigits), unknownDigits))
		
		# The cc segment is the only segment in both 1 and 6
		cc = key[1] - key[6]
		eprint("cc = {}, type is {}".format(cc, type(cc)))
		
		# Use the cc segment to figure out which remaining set is for a 2
		for curDigit in unknownDigits:
			dl = len(curDigit)
			if (dl == 5):
				if cc.issubset(curDigit):
					eprint("Found 5: {}".format(curDigit))
					key[2] = curDigit
					
		unknownDigits.remove(key[2])
		
		# Figure out 5 (it's the only number with 5 segments still lit)
		for curDigit in unknownDigits:
			dl = len(curDigit)
			if (dl == 5):
				key[5] = curDigit
				
		unknownDigits.remove(key[5])
		
		eprint("2 = {}, 5 = {}, num left = {}".format(key[2], key[5], unknownDigits))
		
		# Only 2 unknown digits left
		# All segments of the 5 digit are also in the 9 digit
		if key[5].issubset(unknownDigits[0]):
			key[9] = unknownDigits[0]
			key[0] = unknownDigits[1]
		else:
			key[9] = unknownDigits[1]
			key[0] = unknownDigits[0]
		
		# Now that we have the key to everything, conver the value display to a string of digits
		numStringValueDisplay = ""
		for eachVal in setvaluedisplay:
			for eachKeySet in key:
				if key[eachKeySet] == eachVal:
					numStringValueDisplay += str(eachKeySet)
		
		# Convert the numeric string to an integer, sum for the solution
		print("Num = {}".format(numStringValueDisplay))		
		solution += int(numStringValueDisplay)
	
	print("Solution = {}".format(solution))
		
if __name__ == "__main__":
	main(sys.argv)
