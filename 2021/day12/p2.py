#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def isPathOk(path):
	if (path[0] != "start"):
		return False
		
	afterStart = path[1:]
	if ("start" in afterStart):
		# Start can only be visited once
		#eprint("Can only visit start once")
		return False
		
	# count up small cave visits
	counts = {}
	single2CountNode = None
	for node in afterStart:
		if node.isupper():
			continue
		
		c = counts.get(node, 0)
		c += 1
		counts[node] = c
		
		if (c == 1):
			continue
			
		if (c > 2):
			#eprint("Node {} is more than 2 visit".format(node))
			return False
			
		# C is 2 if we get here, allowed to get here once per path
		if single2CountNode == None:
			single2CountNode = node
		else:
			#eprint("2nd 2 count node, only 1 allowed")
			return False
		
	return True
		


def findNewPaths(mm, currentPath):
	'''
	currentPath = is a list of nodes visited, including the currentLocation
	visitedSoFar = list of lowercase nodes visited, including the currentLocation
	
	returns a list of lists.  inner list is a list of nodes visited ending in end.
	  if empty list returned, cant get to end from this node
	'''
	
	#eprint("findNewPaths(mm, {})".format(currentPath))
	retVal = []
	currentLoc = currentPath[-1]
	possibleNextLocations = mm[currentLoc]
	
	# Great news, u are where u want to be
	if (currentLoc == "end"):
		return [ currentPath ]
		
	
	for nextLoc in possibleNextLocations:
		#eprint("nextLoc is {}".format(nextLoc))
			
		recursivePath = currentPath.copy()
		recursivePath.append(nextLoc)
		
		if not isPathOk(recursivePath):
			continue
		
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
		#eprint("a = {}, b = {}".format(a, b))
		
		aList = mm.get(a, [])
		aList.append(b)
		mm[a] = aList
		bList = mm.get(b, [])
		bList.append(a)
		mm[b] = bList
	
	pp = findNewPaths(mm, [ "start" ])
	#eprint("pp = {}".format(pp))
	print("len of pp = {}".format(len(pp)))
		
if __name__ == "__main__":
	main(sys.argv)
