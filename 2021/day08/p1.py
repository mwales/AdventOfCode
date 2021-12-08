#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	solution = 0
	for singleLine in filedata:
		dontcare, digits = singleLine.split('|')
		for eachDigit in digits.strip().split():
			
			# These 4 digits are easily picked out because they have a unique number of segments on
			dl = len(eachDigit)
			if ( (dl == 2) or (dl == 4) or (dl == 3) or (dl == 7) ):
				solution += 1
				print(eachDigit)
	
	print("Solution = {}".format(solution))

if __name__ == "__main__":
	main(sys.argv)
