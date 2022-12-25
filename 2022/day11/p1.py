#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def customSplit(longstr, otherChars):
	retVal = []
	curString = ""
	for curChar in longstr:
		if curChar in otherChars:
			if (len(curString)):
				retVal.append(curString)
				curString = ""
		else:
			curString += curChar
	if (len(curString)):
		retVal.append(curString)
	return retVal

class Monkey:
	def __init__(self, data):
		monkeyIdParts = customSplit(data[0], " :")
		eprint("Monkey parts: {}".format(monkeyIdParts))
		self.monkeyId = int(monkeyIdParts[1])

		startingParts = customSplit(data[1], " :,")
		eprint("Starting parts = {}".format(startingParts))
		self.items = [ int(x) for x in startingParts[2:] ]

		operationParts = customSplit(data[2], " :=")
		self.operation = operationParts[2:]

		testParts = customSplit(data[3], " :")
		self.divisibleTest = int(testParts[3])

		trueCondParts = customSplit(data[4], ": ")
		falseCondParts = customSplit(data[5], ": ")
		
		self.trueResult = int(trueCondParts[5])
		self.falseResult = int(falseCondParts[5])

		self.numberInvestigations = 0

	def meetOtherMonkeys(self, monkeyList):
		self.monkeyList = monkeyList

	def dump(self, fullDump):
		retData = ""
		retData += "Monkey {}".format(self.monkeyId)
		retData += ": "

		firstItem = True
		for curItem in self.items:
			if firstItem:
				firstItem = False
			else:
				retData += ", "
			retData += str(curItem)

		if fullDump:
			retData += "\n"
			retData += "  Operation: "
			retData += " ".join(self.operation)

			retData += "\n"
			retData += "  Test: divisible by "
			retData += str(self.divisibleTest)

			retData += "\n"
			retData += "  True Result: Throw to monkey "
			retData += str(self.trueResult)

			retData += "\n"
			retData += "  False Result: Throw to monkey "
			retData += str(self.falseResult)

			retData += "\n"
			retData += "  Num Investigations = " 
			retData += str(self.numberInvestigations)

		return retData

	def investigateItems(self):

		oldValues = self.items[:]
		self.items = []
		for curValue in oldValues:
			newVal = self.runOperations(curValue)
			
			newVal = newVal // 3
			eprint("  Worry drops to {}".format(newVal))

			if (newVal % self.divisibleTest == 0):
				# Test is true!
				eprint("Monkey {} test of {} (which is now {}) was True, sending to {}".format(self.monkeyId, curValue, newVal, self.trueResult))
				self.monkeyList[self.trueResult].takeItem(newVal)
			else:
				# Test is false
				eprint("Monkey {} test of {} (which is now {}) was False, sending to {}".format(self.monkeyId, curValue, newVal, self.falseResult))
				self.monkeyList[self.falseResult].takeItem(newVal)
	
			self.numberInvestigations += 1

		eprint("Done inspecting all items")



	def runOperations(self, oldValue):
		if (self.operation[0] == "old"):
			operand1 = oldValue
		else:
			operand1 = int(self.operation[0])

		if (self.operation[2] == "old"):
			operand2 = oldValue
		else:
			operand2 = int(self.operation[2])

		if self.operation[1] == "+":
			retVal = operand1 + operand2
		else:
			retVal = operand1 * operand2

		eprint("Operations {} {} {} = {}".format(operand1, self.operation[1], operand2, retVal))

		return retVal

	def takeItem(self, itemVal):
		eprint("Monkey {} received item {}".format(self.monkeyId, itemVal))
		self.items.append(itemVal)



def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	monkeyData = []
	monkeyList = []
	for line in data:
		if line == "":
			m = Monkey(monkeyData)
			monkeyList.append(m)
			monkeyData.clear()
		else:
			monkeyData.append(line)

	if len(monkeyData) > 2:
		m = Monkey(monkeyData)
		monkeyList.append(m)

	eprint("List of monkeys:")
	for m in monkeyList:
		eprint(m.dump(True))
		m.meetOtherMonkeys(monkeyList)


	for i in range(20):
		for m in monkeyList:
			m.investigateItems()

		eprint("==== Done with round {} ====".format(i+1))
		for m2 in monkeyList:
			eprint(m2.dump(False))

	inspectionTimes = []
	for m in monkeyList:
		inspectionTimes.append(m.numberInvestigations)
	
	eprint("Num investigations: {}".format(inspectionTimes))
	inspectionTimes.sort(reverse=True)
	eprint("Num investigations: {}".format(inspectionTimes))

	solve1 = inspectionTimes[0] * inspectionTimes[1]

	print("Solve 1 = {}".format(solve1))



if __name__ == "__main__":
	main(sys.argv)
