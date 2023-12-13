#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(f"{msg}")


class SpringData:
	def __init__(self, t):
		parts = t.split(" ")
		self.condition = parts[0]
		self.contDamageList = [ int(x) for x in parts[1].split(",") ]
		self.unknown = self.countUnknown()

	def isPlausible(self):
		
		# Minimize damage groups, is this plausible scenario
		#   - check qty of damage groups
		#   - is damage already bigger than max?
		knownDamageGroups = 0
		damageSprintCount = 0
		for c in self.condition:
			

	def countUnknown(self):
		retVal = 0
		for x in self.condition:
			if x == '?':
				retVal += 1
		debug(f"Num unknown in {self.condition} is {retVal}")
		return retVal

	def createSeq(self, testNum):
		leadPadding = "0" * self.unknown
		binaryVal = leadPadding + bin(testNum)[2:]
		binaryVal = binaryVal[-self.unknown:]

		fillData = { '0': '.', '1':'#' }
		
		testSeq = self.condition[:]
		fillIndex = 0
		for i in range(len(testSeq)):
			if testSeq[i] == "?":
				testSeq = testSeq[:i] + fillData[binaryVal[fillIndex]] + testSeq[i+1:]
				fillIndex += 1

		return testSeq

	def isTestSeqValid(self, testSeq):
		debug(f"Testing seq {testSeq} for validity against {self.contDamageList}")
		if (testSeq.find("?") >= 0):
			debug(f"  Test string still has ?")
			return False

		if len(testSeq) != len(self.condition):
			debug(f"  Test string wrong len")
			return False

		damageListIndex = 0
		damageCounter = 0
		for cIndex in range(len(testSeq)):
			if testSeq[cIndex] == '.':
				# Undamaged
				if damageCounter > 0:
					if (damageListIndex >= len(self.contDamageList)):
						debug(f"End of damage group {damageListIndex}, too many groups!")
						return False

					# We must have just ended a damange seq
					if self.contDamageList[damageListIndex] != damageCounter:
						# Incorrect number of damanged springs
						debug(f"  Number of damaged springs {damageCounter} is invalid for {testSeq} at dmgIndex {damageListIndex} of {self.contDamageList}")
						return False
					
					damageCounter = 0
					damageListIndex += 1
			else:
				# Damaged
				damageCounter += 1

		# Is end of list damaged?
		if damageCounter > 0:
			if (damageListIndex >= len(self.contDamageList)):
				debug(f"End of end damage group {damageListIndex}, too many groups!")
				return False

			# We must have just ended a damange seq
			if self.contDamageList[damageListIndex] != damageCounter:
				# Incorrect number of damanged springs
				debug(f"  Seq {testSeq} has invalid number of damaged springs {self.contDamageList} at end")
				return False

			damageListIndex += 1

		if len(self.contDamageList) != damageListIndex:
			debug(f"  Numer of cont damaged spring grounps is invalid in {testSeq} for {self.contDamageList}")
			return False

		debug(f"  Seq {testSeq} is valid for {self.condition} {self.contDamageList}")
		return True
			

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	validCombos = 0
	for t in data:
		vct = 0
		sd = SpringData(t)
		numUnknown = sd.unknown
		for i in range(2 ** numUnknown):
			s = sd.createSeq(i)
			if sd.isTestSeqValid(s):
				vct += 1

		print(f"After {t}, combos = {vct} and sum = {validCombos}")
		validCombos += vct

	print(validCombos)


	

if __name__ == "__main__":
	main(sys.argv)
