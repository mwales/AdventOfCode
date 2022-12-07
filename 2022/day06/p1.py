#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def checkPos(s, p):
	setOfChars = set()
	for i in range(4):
		setOfChars.add(s[p+i])
	
	eprint("Checked {} at {}, set is {} and len {}".format(s, p, setOfChars, len(setOfChars)))

	return (len(setOfChars) == 4)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	for s in data:
		i = 0
		while (i < len(s) - 4):
			if checkPos(s, i):
				print("Marker @ {}".format(i + 4))
				i = len(s)
			i += 1



if __name__ == "__main__":
	main(sys.argv)
