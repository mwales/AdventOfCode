#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def freqAnal(polymer):
	counts = {}
	for c in polymer:
		lettercount = counts.get(c, 0)
		lettercount += 1
		counts[c] = lettercount
	
	minVal = min(counts.values())
	maxVal = max(counts.values())
	
	print("Sol = {}".format(maxVal - minVal))
	
def expand(polymer, rules):
	retVal = polymer[0]
	
	for i in range(1,len(polymer)):
		nextSub = polymer[i-1:i+1]
		eprint("nextSub = {}".format(nextSub))
		
		if nextSub in rules:
			eprint("Adding {}".format(rules[nextSub] + polymer[i]))
			retVal += rules[nextSub] + polymer[i]
		else:
			eprint("No rule, just adding {}".format(polymer[i]))
	
	return retVal
	
def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	polymer = stringData[0]
	
	subRules = {}
	subRulesStrings = stringData[2:]
	for singleRule in subRulesStrings:
		sd = singleRule.split(" -> ")
		subRules[sd[0]] = sd[1]
	
	eprint("Begin polyermer: {}".format(polymer))
	
	for i in range(10):
		polymer = expand(polymer, subRules)
		eprint("After {}, len = {}|, poly = {}".format(i+1, len(polymer), polymer))
	
	freqAnal(polymer)
	
if __name__ == "__main__":
	main(sys.argv)
