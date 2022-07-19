#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm>
using namespace std;

int sum_of_vector(vector<int> input){
	int sum = 0;
	for(int i = 0; i < input.size(); ++i){
		sum += input[i];
	}
	return sum;
}

int solve(const std::vector<int> &&input, const int num_servers)
{
	vector<int> server[num_servers];
	vector<int> temp;
	temp = input;
	sort(temp.begin(), temp.end(), greater<int>());
	// greedy put task into cmputer
	for(int i = 0; i < temp.size(); ++i){
		int min = 99999999;
		int server_ind = 0;
		for(int j = 0; j < num_servers; ++j){
			int temp_min = sum_of_vector(server[j]);
			if(min > temp_min){
				server_ind = j;
				min = temp_min;
			}
		}
		server[server_ind].push_back(temp[i]);
	}

	// cals ans
	int max = 0;
	for(int i = 0; i < num_servers; ++i){
		int temp_max = sum_of_vector(server[i]);
		if(max < temp_max){
			max = temp_max;
		}
	}

	return max;
}

#ifndef KRONOS_TEST
int main()
{

	assert(solve({3, 4, 5, 6}, 3) == 7);
	assert(solve({1, 2, 3, 4}, 3) == 4);
	assert(solve({3, 2, 3, 4, 2, 1}, 4) == 4);
	return 0;
}
#endif
