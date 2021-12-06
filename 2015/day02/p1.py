#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	filedata = f.read().strip().split("\n")
	f.close()
	
	totalWrap = 0
	totalRibbon = 0
	
	for eachDataLine in filedata:
		dimStrs = eachDataLine.split('x')
		l, w, h = [ int(x) for x in dimStrs ]
		
		eprint("l = {}, w = {}, h = {}".format(l, w, h))
		
		area = 2*l*w + 2*w*h + 2*h*l
		smallestSide = min([l * w, l * h, w * h ])
		
		totalWrap += area + smallestSide
		
		smallestPer = 2 * min([l + w, l + h, w + h])
		bow = l * w * h
		
		totalRibbon += smallestPer + bow
		
	print("Total wrap feet = {}".format(totalWrap))
	print("Total ribbon feet = {}".format(totalRibbon))
	

if __name__ == "__main__":
	main(sys.argv)
