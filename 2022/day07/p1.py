#!/usr/bin/env python3

import sys

root_dir = {}

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def updir(path, curDir):
	lastSlash = path.rfind("/")
	newPath = path[:lastSlash]

	newPathParts = newPath.split("/")

	newDir = root_dir
	eprint("  Traversing from root = {}".format(root_dir))
	for subdir in newPathParts:
		if subdir == "":
			continue

		eprint("    subdir = {}".format(subdir))
		newDir = newDir[subdir]


	return newPath, newDir

def addPath(path, curDir, dirname):
	if (path == "/"):
		newPath = "/" + dirname
	else:
		newPath = path + "/" + dirname

	if dirname in curDir:
		eprint("  Directory {} already exists in path!".format(dirname))
		newDir = curDir[dirname]
	else:
		eprint("  Adding directory {}".format(newPath))
		curDir[dirname] = {}
		newDir = curDir[dirname]

	return newPath, newDir

def computeSizeOfDir(dirData):
	curSum = 0
	for curName in dirData.keys():
		eprint("name = {} and dc = {}".format(curName, dirData[curName]))
		if type(dirData[curName]) == type({}):
			curSum += computeSizeOfDir(dirData[curName])
		else:
			curSum += dirData[curName]
	return curSum

def sumOfValidDirSums(dirData, limit):
	superSum = 0
	cs = computeSizeOfDir(dirData)
	if cs < limit:
		superSum += cs
	
	for curName in dirData.keys():
		eprint("  sumOfValidDirSums name = {} and dc = {}".format(curName, dirData[curName]))
		if type(dirData[curName]) == type({}):
			superSum += sumOfValidDirSums(dirData[curName], limit)
	
	return superSum





def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	curDir = root_dir
	curPath = "/"
	for line in data:
		lineparts = line.split()
		if lineparts[0] == "$":
			if lineparts[1] == "cd":
				if lineparts[2] == "/":
					curPath = "/"
					curDir = root_dir
					eprint("Changing to root dir")
				elif lineparts[2] == "..":
					curPath, curDir = updir(curPath, curDir)
					eprint("Changing updir to {}".format(curPath))
				else:
					curPath, curDir = addPath(curPath, curDir, lineparts[2])
					eprint("Went to child path {}".format(curPath))
			elif lineparts[1] == "ls":
				eprint("ls statement")
			else:
				eprint("Massive error on line: {}".format(line))
		else:
			eprint("Dir contents: {}".format(line))
			if (lineparts[0] == "dir"):
				eprint("Ignoring directory name: {}".format(lineparts[1]))
			else:
				eprint("Adding file {} of size {}".format(lineparts[1], lineparts[0]))
				curDir[lineparts[1]] = int(lineparts[0])
	

	eprint("Full root = {}".format(root_dir))

	sumOfAll = sumOfValidDirSums(root_dir, 100000)

	eprint("Sum Of All = {}".format(sumOfAll))

if __name__ == "__main__":
	main(sys.argv)
