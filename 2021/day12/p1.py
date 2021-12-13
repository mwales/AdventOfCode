#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def findNewPaths(mm, currentPath):
	'''
	currentPath = is a list of nodes visited, including the currentLocation
	visitedSoFar = list of lowercase nodes visited, including the currentLocation
	
	returns a list of lists.  inner list is a list of nodes visited ending in end.
	  if empty list returned, cant get to end from this node
	'''
	
	eprint("findNewPaths(mm, {})".format(currentPath))
	retVal = []
	currentLoc = currentPath[-1]
	possibleNextLocations = mm[currentLoc]
	
	# Great news, u are where u want to be
	if (currentLoc == "end"):
		eprint("Special case, end is the end!")
		return [ currentPath ]
	
	for nextLoc in possibleNextLocations:
		#eprint("nextLoc is {}".format(nextLoc))
		if (nextLoc in currentPath) and (nextLoc.islower()):
			#eprint("Can't visit {} twice!".format(nextLoc))
			continue
			
		recursivePath = currentPath.copy()
		eprint("recurPath = {}".format(recursivePath))
		recursivePath.append(nextLoc)
		
		nextPaths = findNewPaths(mm, recursivePath)
		
		if (len(nextPaths) == 0):
			# An empty list means no want to end node from that location
			continue
			
		for eachFuturePath in nextPaths:
			retVal.append(eachFuturePath)
	
	# If we came up with 0 paths, return an empty
	if (len(retVal) == 0):
		return []
	
	# Good case, return the  list of paths we found to the end node
	return retVal 

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	mm = {}	
	for singleLink in stringData:
		a,b = singleLink.split('-')
		
		aList = mm.get(a, [])
		aList.append(b)
		mm[a] = aList
		bList = mm.get(b, [])
		bList.append(a)
		mm[b] = bList
	
	#eprint("mm = {}".format(mm))	
		
	pp = findNewPaths(mm, [ "start" ])
	#print("pp = {}".format(pp))
	print("len of pp = {}".format(len(pp)))
		
if __name__ == "__main__":
	main(sys.argv)
