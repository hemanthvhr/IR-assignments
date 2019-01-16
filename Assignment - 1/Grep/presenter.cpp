#include <iostream>
#include <string>
#include <cstdio>

using namespace std;
//make 
//rm results.txt
//g++ -std=c++11 presenter.cpp -o present
//test ./present 701 320 < mictest.txt >> results.txt
int main(int argc,char* argv[]) {	//args format program-name(implicit), query-id,count
	if(argc < 3) {
		cout << "Error in cl args\n";
		exit(1);
	}
	int i = stoi(argv[2]);
	while(i--) {
		string s;
		cin >> s;
		printf("%s %s\n",argv[1],s.c_str());
	}
	return 0;
}
