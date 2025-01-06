#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def testEquation(finalValue, operandList):
	#print(f"testEquation({finalValue}, {operandList}")
	if len(operandList) == 1:
		# Special case, final operand
		if (finalValue == operandList[0]):
			return finalValue
		else:
			return 0

	# Call self recursively with 1 less operand, attempting all ops for first 2 operands
	
	# addition
	additionList = []
	additionList.append(operandList[0] + operandList[1])
	additionList.extend(operandList[2:])
	if (finalValue == testEquation(finalValue, additionList)):
		return finalValue

	
	# multiply
	mList = []
	mList.append(operandList[0] * operandList[1])
	mList.extend(operandList[2:])
	if (finalValue == testEquation(finalValue, mList)):
		return finalValue

	# concatenation
	cList = []
	cList.append( int(str(operandList[0])+str(operandList[1])) )
	cList.extend(operandList[2:])
	if (finalValue == testEquation(finalValue, cList)):
		return finalValue

	return 0

def solveCase(lineText):
	result, restOfText = lineText.split(":")
	operandList = [int(x) for x in restOfText.strip().split(" ") ]
	print(f"Solve {result} with ops {operandList}")

	resultVal = int(result)

	numOps = len(operandList)
	numPossibleEquations = 2 ** (numOps - 1)

	return testEquation(resultVal, operandList)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	sumVal = 0
	for l in data:
		curVal = solveCase(l)
		sumVal += curVal
		print(f"curVal = {curVal}")

	print(sumVal)

if __name__ == "__main__":
	main(sys.argv)
