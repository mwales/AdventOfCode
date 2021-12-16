#!/usr/bin/env python3

import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


hex2bin = { '0' : '0000',
            '1' : '0001',
            '2' : '0010',
            '3' : '0011',
            '4' : '0100',
            '5' : '0101',
            '6' : '0110',
            '7' : '0111',
            '8' : '1000',
            '9' : '1001',
            'A' : '1010',
            'B' : '1011',
            'C' : '1100',
            'D' : '1101',
            'E' : '1110',
            'F' : '1111' }
	
class BITS:
	def __init__(self, binaryCharList):
		self.version = self.popInteger(binaryCharList, 3)
		self.type = self.popInteger(binaryCharList, 3)
		
		if (self.type == 4):
			eprint("Is literal")
			self.parseLiteral(binaryCharList)
			self.subPackets = None
			self.isLiteral = True
		else:
			eprint("Is operator")
			self.subPackets = []
			self.parseOperator(binaryCharList)
			self.isLiteral = False
			
	def parseLiteral(self, binaryCharList):
		binStr = ""
		while len(binaryCharList) > 0:
			nibbleInd = binaryCharList.pop(0)
			
			for i in range(4):
				binStr += binaryCharList.pop(0)
			
			eprint("binstr so far: {}".format(binStr))
			if nibbleInd == '0':
				eprint("End of nibbles")
				break
			else:
				eprint("More nibbles to come")
		
		self.literalValue = int(binStr, 2)
		eprint("Parse Literal: {}".format(self.literalValue))
		
	def parseOperator(self, binaryCharList):
		typeId = binaryCharList.pop(0)
		
		if typeId == '0':
			# total length in bits of subpackets
			bitsOfSubpackets = self.popInteger(binaryCharList, 15)
			eprint("Operator is type 0, length of subpackets = {}".format(bitsOfSubpackets))
			
			subpacketBinary = binaryCharList[:bitsOfSubpackets]
			del binaryCharList[:bitsOfSubpackets]
			
			while len(subpacketBinary) > 0:
				sp = BITS(subpacketBinary)
				self.subPackets.append(sp)
				
			eprint("Done parsing subpackets, added {} subpackets".format(len(self.subPackets)))
		else:
			# number of sub-packets to parse
			numSubpackets = self.popInteger(binaryCharList, 11)
			eprint("Operator is type 1, number of subpackets = {}".format(numSubpackets))
			
			for i in range(numSubpackets):
				self.subPackets.append(BITS(binaryCharList))
				
	def versionSum(self):
		if self.isLiteral:
			return self.version
		else:
			retval = self.version
			for sp in self.subPackets:
				retval += sp.versionSum()
			return retval
				
			
	def popInteger(self, binaryCharList, numBits):
		intStr = ""
		for i in range(numBits):
			intStr += binaryCharList.pop(0)
			
		eprint("popInteger({}) = {} = {}".format(numBits, intStr, int(intStr, 2)))
		return int(intStr, 2)

def main(argv):
	
	if (len(argv) < 2):
		print("Usage: {} inputfile".format(sys.argv[0]))
		return
	
	f = open(argv[1])
	stringData = f.read().strip().split("\n")
	f.close()
	
	hexData = stringData[0]
	binaryData = []
	for eachChar in hexData:
		binString = hex2bin[eachChar]
		for eachbit in binString:
			binaryData.append(eachbit)
	
	eprint("Bin: {}".format(binaryData))
	
	b = BITS(binaryData)
		
	eprint("Bin: {}".format(binaryData))
	print("Version Sum: {}".format(b.versionSum()))
	
if __name__ == "__main__":
	main(sys.argv)
