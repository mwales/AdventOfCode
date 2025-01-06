#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def evalEquation(operationConfig, operandList):
	curVal = 0
	operationString = ''
	for i in range(len(operandList)):
		# special case, 1st
		if (i == 0):
			curVal = operandList[0]
			operationString += f"{curVal}"
		else:
			curOp = operationConfig & (1 << (i-1))
			if (curOp):
				operationString += f" * {operandList[i]}"
				curVal *= operandList[i]
			else:
				curVal += operandList[i]
				operationString += f" + {operandList[i]}"

	operationString += f" = {curVal}"
	print(f"EVAL: {operationString}")
	return curVal
		

def solveCase(lineText):
	result, restOfText = lineText.split(":")
	operandList = [int(x) for x in restOfText.strip().split(" ") ]
	print(f"Solve {result} with ops {operandList}")

	resultVal = int(result)

	numOps = len(operandList)
	numPossibleEquations = 2 ** (numOps - 1)

	for i in range(numPossibleEquations):
		val = evalEquation(i, operandList)
		if (val == resultVal):
			return resultVal

	return 0

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	sumVal = 0
	for l in data:
		print(f"  solveCase returning {solveCase}")
		sumVal += solveCase(l)

	print(sumVal)

if __name__ == "__main__":
	main(sys.argv)
