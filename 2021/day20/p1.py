#!/usr/bin/env python3

import sys


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def getImageBounds(setData):
	minX = None
	maxX = None
	minY = None
	maxY = None
	
	for eachPt in setData:
		x = eachPt[0]
		y = eachPt[1]
		
		if minX == None:
			minX = maxX = x
			minY = maxY = y
			continue
		
		minX = min(x, minX)
		maxX = max(x, maxX)
		minY = min(y, minY)
		maxY = max(y, maxY)
		
	return minX, maxX, minY, maxY
	
def printMap(md, infiniteField):
	minX, maxX, minY, maxY = getImageBounds(md)
	eprint("x: [{}, {}], y: [{}, {}], if={}".format(minX, maxX, minY, maxY, infiniteField))
	
	for y in range(minY-2, maxY + 3):
		rowText = ""
		for x in range(minX-2, maxX + 3):
			if ( (minX <= x <= maxX) and (minY <= y <= maxY) ):
				# coordinate is within the regular image area
				if (x,y) in md:
					rowText += "#"
				else:
					rowText += "."
			else:
				# coordinate is in the infinite field
				rowText += infiniteField
		
		eprint(rowText)
		
def subPixelEnhance(pt, imgData, iea, infiniteField, minX, maxX, minY, maxY):
	binaryString = ""
	for y in range( pt[1] - 1, pt[1] + 2):
		for x in range( pt[0] - 1, pt[0] + 2):
			if ( (minX <= x <= maxX) and (minY <= y <= maxY) ):
				# coordinate is within the regular image area
				if (x,y) in imgData:
					binaryString += "1"
				else:
					binaryString += "0"
			else:
				# coordinate is in the infinite field
				if (infiniteField == '.'):
					binaryString += "0"
				else:
					binaryString += "1"
	
	decValue = int(binaryString, 2)
	#eprint("subPixelEnhance @ {}, binString={}, decValue={}".format(pt, binaryString, decValue))
	
	if (decValue > len(iea)):
		eprint("Image Enhance Fail. Dec Value = {}, Len = {}".format(decValue, len(iea)))
		return false
	
	#eprint("Enhance for {} has binary {} = {} b10, and is {} in iea".format(pt, binaryString, decValue, iea[decValue]))
	return iea[decValue] == '#'
	
def enhanceImage(imgData, iea, infiniteField):
	retVal = set()
	minX, maxX, minY, maxY = getImageBounds(imgData)
	
	for y in range( minY - 1, maxY + 2):
		for x in range( minX - 1, maxX + 2):
			if subPixelEnhance( (x,y), imgData, iea, infiniteField, minX, maxX, minY, maxY):
				retVal.add( (x,y) )
				
	return retVal

def updateInfiniteField(iea, infiniteField):
	if (infiniteField == '.'):
		binaryString = '000000000'
	else:
		binaryString = "111111111"
		
	decValue = int(binaryString, 2)
	
	return iea[decValue]
	

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	iea = stringData[0]
	
	infiniteField = '.'
	imageData = set()
	y = 0
	x = 0
	for rowText in stringData[2:]:
		x = 0
		for pixel in rowText:
			if pixel == '#':
				imageData.add( (x,y) )
			x += 1
		y += 1
		
	printMap(imageData, infiniteField)
	
	eprint("Len of iea = {}".format(len(iea)))
	
	eprint("Enhance 1 time")
	imageData = enhanceImage(imageData, iea, infiniteField)
	infiniteField = updateInfiniteField(iea, infiniteField)
	printMap(imageData, infiniteField)
	
	eprint("Enhance 2 time")
	imageData = enhanceImage(imageData, iea, infiniteField)
	infiniteField = updateInfiniteField(iea, infiniteField)
	printMap(imageData, infiniteField)
	
	print("Num of pixels lit = {}".format(len(imageData)))

if __name__ == "__main__":
	main(sys.argv)
