#!/usr/bin/env python3

import sys

def debug(msg):
	if True:
		print(msg + "\n")

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	data = f.read().strip().split("\n")
	f.close()

if __name__ == "__main__":
	main(sys.argv)
