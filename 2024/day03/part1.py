#!/usr/bin/env python3

import sys
import re

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip()
	f.close()

	part1sum = 0
	#p = re.compile(r"mul(\d,\d)")
	#p = re.compile(r"mul(\d,\d)")
	p = re.compile(r"mul\(\d*,\d*\)")
	for i in p.finditer(data):
		begin, end = i.span()
		curOp = data[begin:end]
		commaPos = curOp.find(",")
		firstTerm = curOp[4:commaPos]
		secondTerm = curOp[commaPos+1:-1]



		print(f"{firstTerm} x {secondTerm}")

		part1sum += int(firstTerm) * int(secondTerm)

	print(part1sum)
		

if __name__ == "__main__":
	main(sys.argv)
