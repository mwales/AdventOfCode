#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

class Snailfish:
	def __init__(self, line = "[]"):
		# numList is a list of tuples.  it's the number, and the depth
		self.numList = []
		
		curDepth = 0
		for char in line:
			if char == ',':
				continue
			if char == '[':
				curDepth += 1
			elif char == ']':
				curDepth -= 1
			else:
				# Add the number to the list
				self.numList.append( (int(char), curDepth) )
				
	def explodeAndSplit(self):
		# Check for exploders
		for i in range(len(self.numList)):
			if self.numList[i][1] >= 5:
				# eprint("The pair {} and {} must explode".format(self.numList[i][0], self.numList[i+1][0]))
				
				# 3 cases of blowing up.  left side of list, middle of the list, right side of the list
				if i == 0:
					# eprint("Blowin up on the left side of the list")
					self.numList[i] = ( 0, 4 )
					rsNum = self.numList[i+1][0]
					self.numList.pop(i+1)
					self.numList[i+1] = ( rsNum + self.numList[i+1][0], self.numList[i+1][1] )
					
				elif 1 <= i < len(self.numList) - 2:
					# eprint("Blowin up in the middle of the list")
					lsNum = self.numList[i][0]
					rsNum = self.numList[i+1][0]
					self.numList[i - 1] = (self.numList[i - 1][0] + lsNum, self.numList[i - 1][1])
					self.numList.pop(i)
					self.numList[i] = (0,4)
					self.numList[i + 1] = (self.numList[i + 1][0] + rsNum, self.numList[i + 1][1])
				else:
					# eprint("Blowin up on the right side of the list")
					lsNum = self.numList[i][0]
					self.numList[i+1] = ( 0, 4 )
					self.numList[i-1] = ( lsNum + self.numList[i-1][0], self.numList[i-1][1] )
					self.numList.pop(i)
				
				# eprint("After single round of explosion:")
				# eprint(self.toString())
				
				self.explodeAndSplit()
				return
		
		# If you got here, you must not have exploded, check for need to split
		for i in range(len(self.numList)):
			if self.numList[i][0] >= 10:
				# eprint("Need to split {} at {}".format(self.numList[i][0], i))
				
				numToSplit = self.numList.pop(i)
				leftNum = numToSplit[0] // 2
				rightNum = leftNum + (numToSplit[0] % 2)
				
				# Insert right num first
				self.numList.insert(i, ( rightNum, numToSplit[1] + 1 ) )
				self.numList.insert(i, ( leftNum, numToSplit[1] + 1 ) )
				
				self.explodeAndSplit()
				return
	
	def computeMagnitude(self):
		magList = self.numList[:]		
		return self.__internalComputeMagnitude__(magList, 4)
			
	def __internalComputeMagnitude__(self, magList, magLevel):
		#eprint("internalCompute: {} @ level {}".format(magList, magLevel))
		if (magLevel == 0):
			items = [ x[0] for x in magList ]
			return sum(items)
		
		recurseList = []
		
		while(len(magList) > 0):
			ci = magList.pop(0)
			if ci[1] == magLevel:
				# If cur item in list is at the level we are looking for, 
				# next item should be to.  Calculate their magnitude
				ni = magList.pop(0)
				mag = 3 * ci[0] + 2 * ni[0]
				recurseList.append( (mag, magLevel - 1) )
			else:
				recurseList.append(ci)
		
		# Calculate next level down now...
		return self.__internalComputeMagnitude__(recurseList, magLevel - 1)
	
	def add(self, fish2):
		origSelfList = self.numList[:]
		self.numList = []
		
		for f1 in origSelfList:
			self.numList.append( (f1[0], f1[1] + 1) )
			
		for f2 in fish2.numList:
			self.numList.append( (f2[0], f2[1] + 1) )

	def toString(self):
		return str(self.numList)

def main(argv):
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	# Brute force calculate all mags, put all in giant list
	mags = []
	for a in range(len(stringData)):
		for b in range(len(stringData)):
			fishA = Snailfish(stringData[a])
			fishB = Snailfish(stringData[b])
			
			fishA.explodeAndSplit()
			fishB.explodeAndSplit()
			
			fishA.add(fishB)
			fishA.explodeAndSplit()
			
			mags.append(fishA.computeMagnitude())
			
	print("Solve: {}".format(max(mags)))
	
if __name__ == "__main__":
	main(sys.argv)
