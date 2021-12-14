#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	
def freqAnal(polymer, pcs):
	counts = {}
	counts[polymer[0]] = 1
	
	for pair in pcs:
		# Just count the 2nd letters
		c = pair[1]
		
		cc = counts.get(c, 0)
		cc += pcs[pair]
		counts[c] = cc
	
	minVal = min(counts.values())
	maxVal = max(counts.values())
	
	'''
	for key in counts:
		if counts[key] == minVal:
			eprint("min = {} = {}".format(key, counts[key]))
		if counts[key] == maxVal:
			eprint("max = {} = {}".format(key, counts[key]))
	'''
	
	print("Sol = {}".format(maxVal - minVal))
	
def expand(polymerCounts, rules):
	nextCounts = {}
	
	for polys in polymerCounts:
		
		if polys in rules:
			result1 = polys[0] + rules[polys]
			result2 = rules[polys] + polys[1]
			
			#eprint("Reaction for poly {} = {} + {}".format(polys, result1, result2))
			
			rc1 = nextCounts.get(result1, 0)
			rc1 += polymerCounts[polys]
			nextCounts[result1] = rc1
			
			rc2 = nextCounts.get(result2, 0)
			rc2 += polymerCounts[polys]
			nextCounts[result2] = rc2
			#eprint("NC = {}".format(nextCounts))
			
		else:
			# I don't think this code block is ever reached with the input from AoC
			eprint("No reaction for poly {}".format(polys))
			cc = nextCounts.get(polys, 0)
			cc += polymerCounts[polys]
			nextCounts[polys] = cc
			eprint("NC = {}".format(nextCounts))
			
	return nextCounts
	
def convertPolymerToPairCounts(polymer):
	counts = {}
	for i in range(1,len(polymer)):
		nextSub = polymer[i-1:i+1]
		
		curCount = counts.get(nextSub, 0)
		curCount += 1
		counts[nextSub] =  curCount
		
	eprint("Polymer counts = {}".format(counts))
	
	return counts
	
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
	
	pcs = convertPolymerToPairCounts(polymer)
	
	for i in range(10):
		pcs = expand(pcs, subRules)
		#eprint("After {}, pcs = {}".format(i+1, pcs))
	
	print("After 10 iterations")
	freqAnal(polymer, pcs)
	
	for i in range(10, 40):
		pcs = expand(pcs, subRules)
		#eprint("After {}, pcs = {}".format(i+1, pcs))
	
	print("After 40 iterations")
	freqAnal(polymer, pcs)
	
if __name__ == "__main__":
	main(sys.argv)
