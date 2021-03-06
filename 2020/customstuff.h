#pragma once

#include <iostream>
#include <vector>
#include <map>
#include <set>

// VECTOR STUFF

template<typename printableType>
void printVector(std::vector<printableType> v)
{
        std::string retVal;
        bool first = true;
        for(auto const & curItem: v)
        {
                if (!first)
                {
                        std::cout << ",";
                }
                else
                {
                        first = false;
                }

                std::cout << curItem;
        }
}

template<typename printableType>
void debugPrintVector(std::vector<printableType> v)
{
#ifdef AOC_DEBUG
	printVector(v);
#endif
}

template<typename t>
std::vector<t> append(std::vector<t> a, std::vector<t> b)
{
	std::vector<t> retVal;
	retVal = a;
	retVal.insert(retVal.end(), b.begin(), b.end());
	return retVal;
}

template <typename t>
std::vector<t> reverseVector(std::vector<t> const & orig)
{
	std::vector<t> rev;
	for(auto it = orig.rbegin(); it != orig.rend(); it++)
	{
		rev.push_back(*it);
	}
	return rev;
}



template <typename t>
std::vector<t> subVec(std::vector<t> const & vec, int startPos, int endBeforePos = -1)
{
	std::vector<t> retVal;
	
	if (endBeforePos == -1)
	{
		endBeforePos = vec.size();
	}
	for(int i = startPos; i < endBeforePos; i++)
	{
		retVal.push_back(vec[i]);
	}

	return retVal;
}

template <typename t>
std::string toString(std::vector<t> data)
{
	std::string retVal;
	bool first = true;
	for(auto curNum: data)
	{
		if (first)
		{
			first = false;
		}
		else
		{
			retVal += ",";
		}

		retVal += std::to_string(curNum);
	}
	return retVal;
}


template <typename t>
std::ostream& operator<<(std::ostream & os, std::vector<t> data)
{
	bool firstItem = true;
	os << "[";
	for(auto it: data)
	{
		if (firstItem)
		{
			firstItem = false;
		}
		else
		{
			os << ",";
		}

		os << it;
	}
	os << "]";
	return os;
}

// MAP STUFF

template<typename keyType, typename valueType>
void printMap(std::map<keyType, valueType> m)
{
	std::cout << "{";
	bool isFirst = true;
	for(auto singleItem: m)
	{
		if (!isFirst)
		{
			std::cout << ", ";
		}
		else
		{
			isFirst = false;
		}

		std::cout << singleItem.first << " -> " << singleItem.second;
	}

	std::cout << "}";
}

template<typename keyType, typename valueType>
void debugPrintMap(std::map<keyType, valueType> m)
{
#ifdef AOC_DEBUG
	printMap(m);
#endif
}

template <typename keyType, typename valueType>
std::ostream& operator<<(std::ostream & os, std::map<keyType, valueType> data)
{
	bool firstItem = true;
	os << "{";
	for(auto it: data)
	{
		if (firstItem)
		{
			firstItem = false;
		}
		else
		{
			os << ",";
		}

		os << it.first << "->" << it.second;
	}
	os << "}";
	return os;
}

template<typename keyType>
void printSet(std::set<keyType> s)
{
	bool first = true;

	std::cout << "{";
	for(auto it: s)
	{
		if (first)
		{
			first = false;
		}
		else
		{
			std::cout << ",";
		}
		std::cout << it;
	}
	std::cout << "}";
}

template<typename keyType>
void debugPrintSet(std::set<keyType> s)
{
#if AOC_DEBUG
	printSet(s);
#endif
}

template<typename keyType, typename valueType>
std::map<keyType, valueType> mergeMaps(std::map<keyType, valueType> m1,
                                       std::map<keyType, valueType> m2)
{
	std::map<keyType, valueType> retVal;

	for(auto curitem: m1)
	{
		if (retVal.find(curitem.first) == retVal.end())
		{
			// Not in list yet
			retVal[curitem.first] = curitem.second;
		}
		else
		{
			retVal[curitem.first] += curitem.second;
		}
	}

	for(auto curitem: m2)
	{
		if (retVal.find(curitem.first) == retVal.end())
		{
			// Not in list yet
			retVal[curitem.first] = curitem.second;
		}
		else
		{
			retVal[curitem.first] += curitem.second;
		}
	}

	return retVal;
}

template<typename keyType, typename valueType>
std::map<keyType, valueType> reverseMap(std::map<keyType, valueType> m1)
{
	std::map<valueType, keyType> retVal;
	for(auto const & it: m1)
	{
		retVal[it.second] = it.first;
	}
	return retVal;
}

template<typename sortableType>
void insertOrdered(std::vector<sortableType>& origList, sortableType x)
{
        for(auto it = origList.begin(); it != origList.end(); it++)
        {
                if (*it > x)
                {
                        origList.insert(it, x);
                        return;
                }
        }

        // If we get here, empty list?
        origList.push_back(x);
}


template<typename keyType, typename valueType>
std::map<keyType, valueType> multiplyMap(std::map<keyType, valueType> m1, int val)
{
	std::map<keyType, valueType> retVal;

	for(auto curitem: m1)
	{
		retVal[curitem.first] = curitem.second * val;
	}
	return retVal;
}

template<typename keyType, typename valueType>
valueType sumMap(std::map<keyType, valueType> m1)
{
	valueType retVal = 0;

	for(auto curitem: m1)
	{
		retVal += curitem.second;
	}
	return retVal;
}

template <typename t>
std::ostream& operator<<(std::ostream & os, std::set<t> data)
{
	bool firstItem = true;
	os << "{";
	for(auto it: data)
	{
		if (firstItem)
		{
			firstItem = false;
		}
		else
		{
			os << ",";
		}

		os << it;
	}
	os << "}";
	return os;
}

template <typename f, typename s>
std::ostream& operator<<(std::ostream & os, std::pair<f,s> data)
{
	os << "(" << data.first << "," << data.second << ")";
	return os;
}

std::vector<std::string> stringSplit(std::string const & input, char delimeter);
std::vector<std::string> stringSplit(std::string const & input, std::vector<char> const & delimeters);

std::string replaceChar(std::string orig, char before, char after);

std::vector<std::string> readFile(char* filename);


