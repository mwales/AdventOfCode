#!/usr/bin/env python3

import sys

def debug(msg):
	if False:
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
		self.alignStartBeam('>', (0,0) )

	def alignStartBeam(self, pos, direction):
		self.lightDirection = [ direction ]
		self.lightLocation = [ pos ]
		self.energized = set()
		self.energized.add( pos )
		self.lightHistory = set()
		self.lightHistory.add( ( pos, direction ) )


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
	maxE = 0
	for y in range(p.height):
		# Left start
		ptest = Pattern(data)
		ptest.alignStartBeam( (0,y), '>')
		ptest.runBeam()
		maxE = max(maxE, len(ptest.energized) )

		# Right start
		ptest = Pattern(data)
		ptest.alignStartBeam( (p.width - 1,y), '<')
		ptest.runBeam()
		maxE = max(maxE, len(ptest.energized) )

	for x in range(p.width):
		# Top start
		ptest = Pattern(data)
		ptest.alignStartBeam( (x,0), 'V')
		ptest.runBeam()
		maxE = max(maxE, len(ptest.energized) )

		# Bottom start
		ptest = Pattern(data)
		ptest.alignStartBeam( (x, p.height - 1), '^')
		ptest.runBeam()
		maxE = max(maxE, len(ptest.energized) )


	print(maxE)


if __name__ == "__main__":
	main(sys.argv)
