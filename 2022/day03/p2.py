#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def scoreLetter(singleLetter):
	if (singleLetter >= 'a' and singleLetter <= 'z'):
		letterscore = ord(singleLetter) - ord('a') + 1
	else:
		letterscore = ord(singleLetter) - ord('A') + 27
	return letterscore

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	score = 0
	elfGroupIdx = 0
	while(elfGroupIdx < len(data)):
		e1 = data[elfGroupIdx]
		e2 = data[elfGroupIdx + 1]
		e3 = data[elfGroupIdx + 2]

		for singleLetter in e1:
			if ( (singleLetter in e2) and (singleLetter in e3) ):
				eprint("Single letter in all 3 is {}".format(singleLetter))
				score += scoreLetter(singleLetter)
				break

		elfGroupIdx += 3

	print("Total score = {}".format(score))

if __name__ == "__main__":
	main(sys.argv)
