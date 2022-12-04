#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def compareRanges(r1, r2):
	r1pair = r1.split("-")
	r2pair = r2.split("-")

	if (int(r1pair[0]) <= int(r2pair[0]) ) and (int(r1pair[1]) >= int(r2pair[1]) ):
		eprint("r1 = {} and fully contains {}".format(r1, r2))
		return True
	else:
		eprint("r1 {} and r2 {} do not overlap".format(r1, r2))
		return False

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()


	overlapCount = 0
	for ep in data:
		r1, r2 = ep.split(",")

		if (compareRanges(r1, r2)):
			overlapCount += 1
		elif (compareRanges(r2, r1)):
			overlapCount += 1

	print("overlaps = {}".format(overlapCount))

# wrong answer list 283, 595, 491

if __name__ == "__main__":
	main(sys.argv)
