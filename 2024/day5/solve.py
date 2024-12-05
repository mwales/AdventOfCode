#!/usr/bin/env python3

import sys

'''
Notes:
Had I made a function that just sorted the order of the pages from the start,
could have easily solved part 1 and 2.  Even thought about it, but was a little
worried it would be tricky to do (it wasn't).

To create an ordered list, I basically build list 1 item at a time.  First item
is trivial special case, you just add it.  After that, you try to add all new
items at the end of the list, and work yourself back towards the front of the
list.  Checking each iteration if you add it here, does it violate the rules.
'''

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

class PageOrdering:
	def __init__(self, rules):
		self.ruleList = dict()
		for r in rules:
			rdata = [ int(x) for x in r.split("|") ]
			curFirstPage = rdata[0]
			if (curFirstPage in self.ruleList.keys()):
				self.ruleList[curFirstPage].append(rdata[1])
			else:
				self.ruleList[curFirstPage] = [ rdata[1] ]

	def canIAddThisPage(self, curUpdateList, nextPage):
		if (len(curUpdateList) == 0):
			return True

		# Does this new page have a rule?
		if (nextPage in self.ruleList.keys()):
			afterPageList = self.ruleList[nextPage]
			intersectionList = set(afterPageList) & set(curUpdateList)
			if (len(intersectionList) > 0):
				debug(f"Cant add update {nextPage}, it needs to before pages {intersectionList}")
				return False
			else:
				debug(f"You can add {nextPage}, no pages conflict")
				return True
		else:
			debug(f"You can add {nextPage}, no rules for it")
			return True

	def checkOrdering(self, updateList):
		curList = []
		for curPage in updateList:
			if self.canIAddThisPage(curList, curPage):
				curList.append(curPage)
			else:
				return False

		# We added all the pages successfully
		return True

	def orderPages(self, updateList):
		retVal = []
		for curVal in updateList:
			if (updateList[0] == curVal):
				retVal.append(curVal)
				continue

			# Make all possible lists, want to try at end first and work forward
			possibleLists = []
			for i in range(len(retVal)):
				pl = retVal[:]
				pl.insert(i, curVal)
				possibleLists.append(pl)
			atEndList = retVal[:]
			atEndList.append(curVal)
			possibleLists.append(atEndList)

			possibleLists.reverse()

			debug(f"Possible lists: {possibleLists}")

			addNextPage = False
			for curPoss in possibleLists:
				if addNextPage:
					debug("Skipping check of poss {curPoss}")
					continue

				if self.checkOrdering(curPoss):
					debug(f"Order of poss {curPoss} is good")
					addNextPage = True
					retVal = curPoss
					continue
				else:
					debug(f"Order of poss {curPoss} is no good")

		print(f"Built list: {retVal}")
		return retVal

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	dividerRow = data.index("")
	print(dividerRow)

	pageOrderRules = data[:dividerRow]
	updateLists = data[dividerRow+1:]

	print(f"Page order rules {pageOrderRules}")
	print(f"updateLists {updateLists}")

	po = PageOrdering(pageOrderRules)
	print(po.ruleList)

	part1Sum = 0
	part2Sum = 0
	for update in updateLists:
		updateData = [ int(x) for x in update.split(",") ]
		middleElem = len(updateData) // 2 
		if po.checkOrdering(updateData):
			print(f"Good: {updateData}")
			debug(f"Adding element {middleElem} which is {updateData[middleElem]}")
			part1Sum += updateData[middleElem]
		else:
			print(f"Bad: {updateData}")
			correctOrder = po.orderPages(updateData)
			debug(f"Adding element {middleElem} which is {correctOrder[middleElem]}")
			part2Sum += correctOrder[middleElem]

	print(f"Part 1 = {part1Sum}")
	print(f"Part 2 = {part2Sum}")

if __name__ == "__main__":
	main(sys.argv)
