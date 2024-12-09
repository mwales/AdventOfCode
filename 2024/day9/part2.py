#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
		sys.stderr.write(f"{msg}\n")


class disk:
	def __init__(self, initialMap):
		curFileId = 0
		curPos = 0
		self.initialFileMap = []
		self.emptyList = []
		self.fileBlocks = []
		for i in range(0,len(initialMap),2):
			curFileLen = int(initialMap[i])
			self.initialFileMap.append( (curPos, curFileLen) )
			curPos += curFileLen

			for nb in range(curFileLen):
				self.fileBlocks.append(curFileId)


			if (i+1) < len(initialMap):
				numEmpty = int(initialMap[i+1])
				self.emptyList.append( (curPos,numEmpty) )
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

		print(f"Empties: {self.emptyList}")

	def moveFile(self, fileId, emptyId):
		fileLen = self.initialFileMap[fileId][1]
		emptyPos, emptyLen = self.emptyList[emptyId]
		debug(f"Moving file {fileId} to {emptyPos}")
		
		# Write the file block data
		for i in range(fileLen):
			# Write the file block data
			self.fileBlocks[i + emptyPos] = fileId

			# Erase the old file block data
			self.fileBlocks[self.initialFileMap[fileId][0] + i] = None

		# Fixup the empty list
		if (emptyLen > fileLen):
			# Move the position and size of empty
			newEmptyPos = emptyPos + fileLen
			newEmptyLen = emptyLen - fileLen
			self.emptyList[emptyId] = (newEmptyPos, newEmptyLen)
		else:
			# We used up all the empty space, remove from empty list
			self.emptyList.pop(emptyId)

		#self.printDisk()

	def tryToDefrag(self, fileId):
		debug(f"tryToDefrag({fileId}")
		fileIdToMovePos, fileIdToMoveSize = self.initialFileMap[fileId]

		for emptyIndex, emptyInfo in enumerate(self.emptyList):
			emptyPos, emptyLen = emptyInfo

			if (emptyLen >= fileIdToMoveSize):

				if (emptyPos > fileIdToMovePos):
					debug("First empty is to the right")
					return

				self.moveFile(fileId, emptyIndex)
				return
		debug(f"Nowhere to move the file")

	
	def defrag(self):
		for fileIdToMove in range(len(self.initialFileMap)-1,-1,-1):
			self.tryToDefrag(fileIdToMove)
				
	def computeChecksum(self):
		cs = 0
		for pos, fileId in enumerate(self.fileBlocks):
			if (fileId == None):
				continue
			cs += pos * fileId
		return cs

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	d = disk(data[0])
	debug(d.initialFileMap)

	#d.printDisk()
	
	print("Defragin")
	d.defrag()

	print("Done")
	print(f"Part 2 = {d.computeChecksum()}")
	

if __name__ == "__main__":
	main(sys.argv)
