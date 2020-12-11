#include <iostream>
#include <vector>
#include <map>
#include <cstdlib>
#include <set>
#include <fstream>

#include "../customstuff.h"

#ifdef AOC_DEBUG
	#define DEBUG std::cout
#else
	#define DEBUG if(0) std::cout
#endif

int part1(std::vector<int> const & nums)
{
	int adapter1Jolt = 0;
	int adapter3Jolt = 0;

	int lastJoltage = 0;
	for(auto curNum: nums)
	{
		if (curNum - lastJoltage == 1)
		{
			adapter1Jolt++;
		}

		if (curNum - lastJoltage == 3)
		{
			adapter3Jolt++;
		}

		lastJoltage = curNum;
	}

	// last plug
	adapter3Jolt += 1;

	DEBUG << "1 jolts = " << adapter1Jolt << std::endl;
	DEBUG << "3 jolts = " << adapter3Jolt << std::endl;

	return adapter1Jolt * adapter3Jolt;
}

bool isChainValid(std::vector<int> const & chain)
{
	int lastNum = 0;
	for(auto curNum: chain)
	{
		if ( (curNum - lastNum > 3) || (curNum == lastNum) )
		{
			DEBUG << "Invalid Chain: ";

			debugPrintVector(chain);

			DEBUG << std::endl;
			return false;
		}

		lastNum = curNum;
	}

	return true;
}

void printVVList(std::vector<std::vector<int> > vvList)
{
	DEBUG << "VV List **********************************" << std::endl;
	for(auto singleList: vvList)
	{
		debugPrintVector(singleList);
		DEBUG << std::endl;
	}
}

void filterLists(std::vector<std::vector<int> > & vvList)
{
	int i = 0;
	while(i < vvList.size())
	{
		if (isChainValid(vvList[i]))
		{
			i++;
			continue;
		}

		// not valid, remove
		vvList.erase(vvList.begin() + i);
	}

}

int part2(std::vector<int> const & origList)
{
	std::vector<std::vector<int> > seqLists;
	int lastNum = *origList.rbegin();
	DEBUG << "Last number in list is " << lastNum << std::endl;
	
	for(auto curNum: origList)
	{
		// Always try to create a list that starts with curNum if less than 3
		if (curNum <= 3)
		{
			DEBUG << "Special Case: numbers less than 3" << std::endl;
			std::vector<int> temp;
			temp.push_back(curNum);
			seqLists.push_back(temp);
		}

		if (lastNum == curNum)
		{
			// Special case for last num, always gets added to end of all seq lists
			DEBUG << "Special Case: last number in list" << std::endl;
			
			std::vector<std::vector<int> > seqCopy = seqLists;
			seqLists.clear();
			for(auto singleList: seqCopy)
			{
				singleList.push_back(curNum);
				seqLists.push_back(singleList);
			}
		}
		else
		{
			// Numbers in the middle of the list.  Keep orig list, plus add a new list
			//   with new number for every number in the middle. We will filter bad
			//   lists out later
			std::vector<std::vector<int> > seqCopy = seqLists;
			for(auto prevSeqList: seqCopy)
			{
				prevSeqList.push_back(curNum);

				DEBUG << "Going to add list: ";

				debugPrintVector(prevSeqList);

				DEBUG << std::endl;

				seqLists.push_back(prevSeqList);
			}
		}


		printVVList(seqLists);

		DEBUG << "FILTERING" << std::endl;
		filterLists(seqLists);

		printVVList(seqLists);
	}

	return seqLists.size();
}

int main(int argc, char** argv)
{

	if (argc < 2)
	{
		std::cerr << "Provide filename" << std::endl;
		return 0;
	}

	std::ifstream infile(argv[1]);

	std::vector<int> adapterList;

	while(infile.is_open())
	{
		std::string text;
		std::getline(infile,text);


		// out of output
check_for_eof:
      if (infile.eof())
		{
			break;
		}

		DEBUG << text << std::endl;

		int curNum = atoi(text.c_str());
		insertOrdered(adapterList,curNum);
	}

	printVector(adapterList);
	std::cout << std::endl;

	int pt1 = part1(adapterList);

	std::cout << "Part 1 = " << pt1 << std::endl;

	infile.close();

	return 0;
}
