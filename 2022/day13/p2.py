#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

class DistressSignal:
	def __init__(self, pd):
		self.valItems = []
		eprint("DistressSignal( {} )".format(pd))

		startPos = pd.find("[") + 1
		endPos = pd.rfind("]") + 1

		#eprint("List of Data: {}".format(pd[startPos:endPos-1]))
		self.parseList(pd[startPos:endPos-1])

	def parseList(self, listOfData):
		#eprint("parseList({})".format(listOfData))

		braceLevel = 0
		curItemStr = ""
		eatAComma = False
		for pos in range(len(listOfData)):
			curItem = listOfData[pos]
			#eprint("Processing char: {}".format(curItem))
			if (eatAComma):
				if (curItem == ","):
					eprint("Ate a comma")
					eatAComma = False
				continue

			if (braceLevel == 0) and (curItem == ","):
				self.valItems.append(curItemStr)
				curItemStr = ""
			elif (braceLevel == 0) and (curItem == '['):
				startOfBrace = pos
				braceLevel += 1
			elif (curItem == '['):
				braceLevel += 1
			elif (braceLevel == 1) and (curItem == ']'):
				# end of sublist
				eprint("Start brace @ {}, end brace @ {}, substr = {}".format(startOfBrace, pos, listOfData[startOfBrace:pos+1]))
				self.valItems.append(DistressSignal( listOfData[startOfBrace:pos+1] ))
				braceLevel = 0
				curItemStr = ""
				eatAComma = True
			elif (curItem == ']') and (braceLevel <= 0):
				eprint("Error parsiong {}, negative brace level @ {}".format(listOfData, pos))
			elif (curItem == ']'):
				braceLevel -= 1
			else:
				curItemStr += curItem

		if len(curItemStr) > 0:
			eprint("  Adding {} to the itemVals".format(curItemStr))
			self.valItems.append(curItemStr)

		eprint("List of items parsed (strings): {}".format(self.valItems))

	def __repr__(self):
		retVal = "DS["
		firstItem = True
		for curItem in self.valItems:
			if firstItem:
				firstItem = False
			else:
				retVal+=","
			retVal += str(curItem)
		retVal += ']'
		return retVal

	def __eq__(self, rhs):
		eprint("Comparing {} and {} for equality!".format(self, rhs))

		if (type(self) != type(rhs)):
			return False

		if (len(self.valItems) != len(rhs.valItems)):
			return False

		for i in range(len(self.valItems)):
		
			lhsItem = self.valItems[i]
			rhsItem = rhs.valItems[i]

			if (type(lhsItem) != type(rhsItem)):
				return False
			if lhsItem != rhsItem:
				return False

		# No differences!
		return True

	def __ne__(self, rhs):
		return ( not (self == rhs))

	def __lt__(self, rhs):
		eprint("Is {} less than {}?".format(self, rhs))
		if (self == rhs):
			eprint("  Is {} less than {}, no they are equal!".format(self, rhs))
			return False

		if (type(self) != type(rhs)):
			eprint("  Comparing {} and {}, they are differnt types!".format(self, rhs))
			tempLhsItem = self
			tempRhsItem = DistressSignal("[ {} ]".format(rhs))
			return tempLhsItem < tempRhsItem

		for i in range(len(self.valItems)):
			eprint("  Comparing {} and {} at index {}".format(self, rhs, i))

			lhsItem = self.valItems[i]
			if (len(rhs.valItems) <= i):
				eprint("  Is {} less than {}, no because at index {} rhs is out of items".format(self, rhs, i))
				# Not enough items on rhs
				return False
			rhsItem = rhs.valItems[i]

			# Are they both integers?
			if (type(lhsItem) == type(rhsItem)):
				eprint("  Both items are same exact type {} and {}".format(type(lhsItem), type(rhsItem)))
				if (type(lhsItem) == str):
					# Both are integers
					if int(lhsItem) < int(rhsItem):
						eprint("    Item {} < {}, returning true".format(lhsItem, rhsItem))
						return True
					elif (int(lhsItem) != int(rhsItem)):
						eprint("    Item {} != {}, so must be >, returning false".format(lhsItem, rhsItem))
						return False
				else:
					# Both are lists
					eprint("  Both items must be lists!")
					if lhsItem < rhsItem:
						return True
					if lhsItem != rhsItem:
						return False

				# else, they are equal, move onto the next item in list to compare
			else:
				eprint("  Items {} and {} are of tyep {} and {}".format(lhsItem, rhsItem, type(lhsItem), type(rhsItem)))
				# They are differnet types, one is an integer, and one is a list
				# conver the integer to list of 1 and then compare
				if (type(lhsItem) == str):
					tempLhsItem = DistressSignal("[ {} ]".format(lhsItem))
				else:
					tempLhsItem = lhsItem

				if (type(rhsItem) == str):
					tempRhsItem = DistressSignal("[ {} ]".format(rhsItem))
				else:
					tempRhsItem = rhsItem

				eprint("    We have now promoted the cmoparison to {} vs {}".format(tempLhsItem, tempRhsItem))

				if (tempLhsItem < tempRhsItem):
					return True
				if (tempLhsItem != tempRhsItem):
					return False

				# if they are equal, continue on to the next item in valItems list...

		# Uh oh, we are out of items, and we know we aren't equal, one must have more items!
		eprint("Comparison of {} and {} is down to the number of items!".format(self, rhs))
		if (len(self.valItems) < len(rhs.valItems)):
			return True
		else:
			return False
		


				

				

def DSCompare(lhs, rhs):
	if (lhs == rhs):
		return 0
	elif (lhs < rhs):
		return -1
	else:
		return 1


def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	signalList = []
	sumIdx = 0
	curIdx = 0
	for i in range(0, len(data), 3):
		curIdx += 1
		left = data[i]
		right = data[i+1]
		eprint("IDX {}, first= {}, second= {}".format(curIdx, left, right))

		signalList.append(DistressSignal(left))
		signalList.append(DistressSignal(right))

	special2Signal = DistressSignal("[[2]]")
	special6Signal = DistressSignal("[[6]]")

	signalList.append(special2Signal)
	signalList.append(special6Signal)

	eprint("==========================")
	eprint("Before Sort:")
	for ds in signalList:
		eprint(ds)


	signalList.sort()

	eprint("==========================")
	eprint("After Sort:")
	for ds in signalList:
		eprint(ds)

	pos2 = None
	pos6 = None
	
	for i in range(len(signalList)):
		if signalList[i] == special2Signal:
			pos2 = i+1
		if signalList[i] == special6Signal:
			pos6 = i + 1

	print("2sig x 6sig = {} x {} = {}".format(pos2, pos6, pos2 * pos6))





if __name__ == "__main__":
	main(sys.argv)
