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
		
		digits = alldigitstogether.strip().split()
		
		# a dictionary mapping digits to sets
		key = {}
		setdigits = [ wordToSet(x) for x in digits ]
		setvaluedisplay = [ wordToSet(x) for x in valuedisplay.strip().split() ]
		
		eprint("len = {}, setdigits = {}".format(len(setdigits), setdigits))
		
		for eachDigit in setdigits:
			dl = len(eachDigit)
			if (dl == 2):
				key[1] = eachDigit
			elif (dl == 4):
				key[4] = eachDigit
			elif (dl == 3):
				key[7] = eachDigit
			elif (dl == 7):
				key[8] = eachDigit
				
		setdigits.remove(key[1])
		setdigits.remove(key[4])
		setdigits.remove(key[7])
		setdigits.remove(key[8])
		
		eprint("len = {}, setdigits = {}".format(len(setdigits), setdigits))
	
		eprint("AnsKey = {}".format(key))
		
		aa = key[7] - key[1]
		eprint("aa = {}".format(aa))
		
		# Figure out 3 and 6
		for curDigit in setdigits:
			dl = len(curDigit)
			if (dl == 5):
				if key[1].issubset(curDigit):
					key[3] = curDigit
			if (dl == 6):
				if not key[1].issubset(curDigit):
					key[6] = curDigit
					
		eprint("3 = {}".format(key[3]))
		eprint("6 = {}".format(key[6]))
		
		eprint("len = {}, setdigits = {}".format(len(setdigits), setdigits))
		
		setdigits.remove(key[3])
		setdigits.remove(key[6])
		
		eprint("len = {}, setdigits = {}".format(len(setdigits), setdigits))
		
		cc = key[1] - key[6]
		eprint("cc = {}, type is {}".format(cc, type(cc)))
		
		# Figure out 2
		for curDigit in setdigits:
			dl = len(curDigit)
			if (dl == 5):
				if cc.issubset(curDigit):
					eprint("Found 5: {}".format(curDigit))
					key[2] = curDigit
					
		setdigits.remove(key[2])
		
		# Figure out 5
		for curDigit in setdigits:
			dl = len(curDigit)
			if (dl == 5):
				key[5] = curDigit
				
		setdigits.remove(key[5])
		
		eprint("2 = {}, 5 = {}, num left = {}".format(key[2], key[5], setdigits))
		
		if key[5].issubset(setdigits[0]):
			key[9] = setdigits[0]
			key[0] = setdigits[1]
		else:
			key[9] = setdigits[1]
			key[0] = setdigits[0]
		
		numStringValueDisplay = ""
		for eachVal in setvaluedisplay:
			for eachKeySet in key:
				if key[eachKeySet] == eachVal:
					numStringValueDisplay += str(eachKeySet)
			
		print("Num = {}".format(numStringValueDisplay))
		
		solution += int(numStringValueDisplay)
	
	print("Solution = {}".format(solution))
		
if __name__ == "__main__":
	main(sys.argv)
