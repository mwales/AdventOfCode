#!/usr/bin/env python3

import sys

class disk:
	def __init__(self, initialMap):
		curFileId = 0
		curPos = 0
		self.initialFileMap = []
		self.fileBlocks = []
		for i in range(0,len(initialMap),2):
			curFileLen = int(initialMap[i])
			self.initialFileMap.append( (curPos, curFileLen) )
			curPos += curFileLen

			for nb in range(curFileLen):
				self.fileBlocks.append(curFileId)


			if (i+1) < len(initialMap):
				numEmpty = int(initialMap[i+1])
				curPos += numEmpty

				for nb in range(numEmpty):
					self.fileBlocks.append(None)

			curFileId += 1
					


	def printDisk(self):
		blockData = ""
		for i in range(len(self.fileBlocks)):
			if (self.fileBlocks[i] == None):
				blockData += "."
			else:
				blockData += str(self.fileBlocks[i])
		print(blockData)

	def defragCell(self):
		findRear = None
		findFirstEmpty = None
		for i, contents in enumerate(self.fileBlocks):
			if (contents == None):
				findFirstEmpty = i
				break

		#print("r search")
		for i in range(len(self.fileBlocks) - 1, -1, -1):
			#print(f"i = {i} which is {self.fileBlocks[i]}")
			if (self.fileBlocks[i]):
				findRear = i
				break

		if (findRear < findFirstEmpty):
			# It's already defragged
			print(f"defragging stopping cause rear = {findRear} and front = {findFirstEmpty}")
			return False
		else:
			self.fileBlocks[findFirstEmpty] = self.fileBlocks[findRear]
			self.fileBlocks[findRear] = None
			return True

	def computeChecksum(self):
		cs = 0
		for pos, fileId in enumerate(self.fileBlocks):
			if (fileId == None):
				break
			cs += pos * fileId
		return cs

def debug(msg):
	if True:
		sys.stderr.write(f"{msg}\n")

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	d = disk(data[0])
	print(d.initialFileMap)

	#d.printDisk()

	while(d.defragCell()):
		continue
		#d.printDisk()

	print("Done")
	print(f"Part 1 = {d.computeChecksum()}")
	

if __name__ == "__main__":
	main(sys.argv)
