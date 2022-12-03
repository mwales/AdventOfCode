#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	score = 0
	for rs in data:
		eprint("Len of ruck = {}".format(len(rs)))
		c1 = rs[0:len(rs)//2]
		c2 = rs[len(rs)//2:]
		
		eprint("p1 = {} and p2 = {}".format(c1, c2))

		idx = 0
		while (idx < len(c1)):
			singleLetter = c1[idx]
			if singleLetter in c2:
				if (singleLetter >= 'a' and singleLetter <= 'z'):
					letterscore = ord(singleLetter) - ord('a') + 1
				else:
					letterscore = ord(singleLetter) - ord('A') + 27
				eprint("letter {} is unique, score = {}".format(singleLetter, letterscore))
				score += letterscore
				idx = len(c1)
			idx += 1

	print("Total score = {}".format(score))

if __name__ == "__main__":
	main(sys.argv)
