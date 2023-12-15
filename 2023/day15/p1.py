#!/usr/bin/env python3

import sys

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

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

	parts = data[0].split(",")

	hv = 0
	for sp in parts:
		hv += lavaHash(sp)
	
	print(hv)
if __name__ == "__main__":
	main(sys.argv)
