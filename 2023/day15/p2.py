#!/usr/bin/env python3

import sys

class Box:
	def __init__(self, pos):
		self.pos = pos
		self.lensOrder = []
		self.focalLen = {}

	def addLens(self, label, fl):
		if (label not in self.lensOrder):
			self.lensOrder.append(label)
		self.focalLen[label] = fl

	def removeLens(self, label):
		if (label in self.lensOrder):
			self.lensOrder.remove(label)

	def isEmpty(self):
		return len(self.lensOrder) == 0

	def powerVal(self):
		powerIndex = 0
		retVal = 0
		for l in self.lensOrder:
			powerIndex += 1
			retVal += powerIndex * self.focalLen[l]
		debug(f"Box {self.pos} has power of {retVal}")
		return retVal

	def __repr__(self):
		retVal = f"Box {self.pos}: "
		for l in self.lensOrder:
			retVal += l
			retVal += "="
			retVal += str(self.focalLen[l])
			retVal += ", "
		return retVal

gBoxes = []

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def lavaHash(t):
	retVal = 0
	for sc in t:
		retVal += ord(sc)
		#debug(f"  increases to {retVal}")
		retVal *= 17
		#debug(f"  * 17 to {retVal}")
		retVal %= 256
		debug(f"  HV @ {sc} = {retVal}")
	return retVal

def setInstruction(t):
	eqSep = t.find('=')
	label = t[:eqSep]
	boxNum = lavaHash(label)
	focalVal = int(t[eqSep+1:])
	debug(f"{t} is a set instruction, box {boxNum} with fl {focalVal}")
	gBoxes[boxNum].addLens(label, focalVal)

def popInstruction(t):
	label = t[:-1]
	boxNum = lavaHash(label)
	debug(f"{t} is a pop instruction, box {boxNum}")
	gBoxes[boxNum].removeLens(label)



def processInstruction(t):
	if (t.find('=') > 1):
		setInstruction(t)
	else:
		popInstruction(t)

def printBoxes():
	for b in gBoxes:
		if not b.isEmpty():
			print(b)

def computeAllFocusPowers():
	fp = 0
	bIndex = 0
	for b in gBoxes:
		bIndex += 1
		fp += (bIndex) * b.powerVal()
	return fp
	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	parts = data[0].split(",")
	
	for i in range(256):
		b = Box(i)
		gBoxes.append(b)

	for sp in parts:
		debug(f"Executing: {sp}")

		processInstruction(sp)
	
		printBoxes()
	
	fp = computeAllFocusPowers()
	print(f"Focal Power = {fp}")

if __name__ == "__main__":
	main(sys.argv)
