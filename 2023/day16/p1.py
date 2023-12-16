#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		#sys.stderr.write(f"{msg}\n")
		print(f"{msg}")


class Pattern:
	def __init__(self, data):
		self.width = len(data[0])
		self.height = len(data)
		debug(f"New pattern that is {self.width} x {self.height}")
		self.data = {}
		for y in range(self.height):
			for x in range(self.width):
				if data[y][x] != '.':
					self.data[ (x,y) ] = data[y][x]
		self.setupDestMap()
		self.beginLightBeam()
	
	def isPointInRange(self, p):
		(x,y) = p
		if ( (x < 0) or (x >= self.width) ):
			return False

		if ( (y < 0) or (y >= self.height) ):
			return False
		return True

	def getPoint(self, p):
		return self.data.get(p, '.')
	
	def setPoint(self, p, val):
		self.data[p] = val

	def beginLightBeam(self):
		self.lightDirection = [ ">" ]
		self.lightLocation = [ (0,0) ]
		self.energized = set()
		self.energized.add( (0,0) )
		self.lightHistory = set()
		self.lightHistory.add( ( (0,0),'>' ) )

	def setupDestMap(self):
		self.destPosMap = { ('>', '.'): [ (1, 0) ],
		                    ('^', '.'): [ (0, -1) ],
		                    ('<', '.'): [ (-1, 0) ],
		                    ('V', '.'): [ (0, 1) ],
		                    ('>', '|'): [ (0, 1), (0, -1) ],
		                    ('^', '|'): [ (0, -1) ],
		                    ('<', '|'): [ (0, 1), (0, -1) ],
		                    ('V', '|'): [ (0, 1) ],
		                    ('>', '-'): [ (1, 0) ],
		                    ('^', '-'): [ (-1, 0), (1,0) ],
		                    ('<', '-'): [ (-1, 0) ],
		                    ('V', '-'): [ (-1, 0), (1,0) ],
		                    ('>', '/'): [ (0, -1) ],
		                    ('^', '/'): [ (1, 0) ],
		                    ('<', '/'): [ (0, 1) ],
		                    ('V', '/'): [ (-1, 0) ],
		                    ('>', '\\'): [ (0, 1) ],
		                    ('^', '\\'): [ (-1, 0) ],
		                    ('<', '\\'): [ (0, -1) ],
		                    ('V', '\\'): [ (1, 0) ] }

		self.destDirMap = { ('>', '.'): [ '>' ],
		                    ('^', '.'): [ '^' ],
		                    ('<', '.'): [ '<' ],
		                    ('V', '.'): [ 'V' ],
		                    ('>', '|'): [ 'V', '^' ],
		                    ('^', '|'): [ '^' ],
		                    ('<', '|'): [ 'V', '^' ],
		                    ('V', '|'): [ 'V' ],
		                    ('>', '-'): [ '>' ],
		                    ('^', '-'): [ '<', '>' ],
		                    ('<', '-'): [ '<' ],
		                    ('V', '-'): [ '<', '>' ],
		                    ('>', '/'): [ '^' ],
		                    ('^', '/'): [ '>' ],
		                    ('<', '/'): [ 'V' ],
		                    ('V', '/'): [ '<' ],
		                    ('>', '\\'): [ 'V' ],
		                    ('^', '\\'): [ '<' ],
		                    ('<', '\\'): [ '^' ],
		                    ('V', '\\'): [ '>' ] }


		

	def iterateLightBeam(self):
		newLightDirection = []
		newLightLocation = []
		for i in range(len(self.lightDirection)):
			curDir = self.lightDirection[i]
			curPos = self.lightLocation[i]
			curTile = self.getPoint(curPos)

			nextPosDelta = self.destPosMap[(curDir, curTile)]
			nextDirList = self.destDirMap[(curDir, curTile)]

			j = 0
			for j in range(len(nextPosDelta)):
				npd = nextPosDelta[j]
				ndir = nextDirList[j]

				newX = curPos[0] + npd[0]
				newY = curPos[1] + npd[1]
				
				p = (newX, newY)
				historyEntry = ( (newX, newY), ndir )
				if self.isPointInRange(p) and (historyEntry not in self.lightHistory):
					newLightLocation.append(p)
					newLightDirection.append(ndir)
					self.lightHistory.add(historyEntry)

		debug(f"After light iteration:")
		debug(f"  {newLightDirection}")
		debug(f"  {newLightLocation}")

		self.lightDirection = newLightDirection
		self.lightLocation = newLightLocation

	def runBeam(self):
		while(len(self.lightLocation) > 0):
			self.iterateLightBeam()

			for p in self.lightLocation:
				self.energized.add(p)

			


	def __repr__(self):
		retData = f"** Pattern is {self.width} x {self.height}\n"
		for y in range(self.height):
			for x in range(self.width):
				retData += self.getPoint( (x,y) )
			retData += "\n"

		retData += f"LightLoc: {self.lightLocation}\n"
		retData += f"LightPos: {self.lightDirection}\n"
		retData += f"Energized: {self.energized}\n"
		return retData



def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	p = Pattern(data)

	debug(p)
	p.runBeam()

	debug(p)

	print(len(p.energized))


if __name__ == "__main__":
	main(sys.argv)
