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

	mulEnabled = True
	opList = []

	part2Sum = 0
	#p = re.compile(r"mul(\d,\d)")
	#p = re.compile(r"mul(\d,\d)")
	p = re.compile(r"mul\(\d*,\d*\)")
	for i in p.finditer(data):
		begin, end = i.span()
		curOp = data[begin:end]
		opList.append( (begin, curOp) )

	print("Finding the do's")
	p2 = re.compile(r"do\(\)")
	for i in p2.finditer(data):
		begin, end = i.span()
		curOp = data[begin:end]
		opList.append( (begin, curOp) )
		print(f"{curOp} at {begin}:{end}")

	print("Finding the donts")
	p3 = re.compile(r"don\'t\(\)")
	for i in p3.finditer(data):
		begin, end = i.span()
		curOp = data[begin:end]
		opList.append( (begin, curOp) )
		print(f"{curOp} at {begin}:{end}")

	print(f"Raw op list = {opList}")
	
	opList.sort()
	print(f"Sorted op list = {opList}")

	for startPos, curOp in opList:
		if (curOp == "do()"):
			mulEnabled = True
			print("Enabling mul")
			continue
		
		if (curOp == "don't()"):
			mulEnabled = False
			print("Disabling mul")
			continue
	
		commaPos = curOp.find(",")
		firstTerm = curOp[4:commaPos]
		secondTerm = curOp[commaPos+1:-1]

		if (mulEnabled):
			print(f"Mul {curOp}")
			part2Sum += int(firstTerm) * int(secondTerm)
		else:
			print(f"Mul disabled, ignoring {curOp}")

	print(part2Sum)

if __name__ == "__main__":
	main(sys.argv)
