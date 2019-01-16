#include <iostream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <cstdio>
#include <time.h>
#include <unordered_map>	
#include <unordered_set>
#include <fstream>

using namespace std;
//make
//rm results.txt
//g++ -std=c++11 -o search searcher.cpp


const char* benchm = "output.txt";
const char* results = "results.txt";
const char* queries = "query.txt";
const char* presenter = "present";
const int noquer = 82;
const char* loc = "alldocs/*";
int tot = 0;

void hasher(unordered_map < int , unordered_set < string > > & output,unordered_map<int,double> &A,unordered_map <int ,int >& B) {
	fstream file;
	int id;
	string s;
	unordered_map< int ,int > rel;
	file.open(benchm);
	for(int i=0;i<7500;i++) {
		file >> id >> s;
		output[id].emplace(s);
	}	rel[id] = 0;
	file.close();
	file.open(results);
	for(int i=0;i<tot;i++) {
		file >> id >> s;
		int x = output[id].count(s);
		rel[id] += x;
	}
	file.close();
	
	printf("Query ID	Time(in ms)	       Precision(%c)             Recall(%c)\n",'%','%');
	for(int i=701;i<851;i++) {
		if(B.find(i)==B.end()) continue;	//output for only valid queries
		double p,r;
		r = (double)rel[i]/(double)50;
		r*=(double)100.0;
		if(B[i]) p = (double)rel[i]/(double)B[i];
		else p = 0;
		p*=(double)100.0;
		double a;
		if(A.find(i)!=A.end()) a = A[i];
		else a = 0;
		a *= (double)1000;
		printf("%d		%.3lf			%.2lf			%.2lf\n",i,a,p,r);
	}
	
}

int main() {
	int id;
	char *command,*input,*ide;
	char cc[7];	 
	clock_t start,end;
	unordered_map<int,int> B;
	unordered_map<int ,double> A;
	unordered_map < int , unordered_set < string > > output;
	for(int i=0;i<noquer;i++) {
		string s;
		getline(cin,s);
		input = new char[s.size()+1];
		command = new char[s.size()+450];
		strcpy(input,s.c_str());
		command[0]='g';command[1]='r';command[2]='e';command[3]='p';command[4]=' ';command[5]='\0';
		char *token = strtok(input," ");
		id = stoi(token);
		ide = token;
		token = strtok(NULL," ");
		
		strcat(command,token);
		strcat(command," ");
		strcat(command,loc);
		strcat(command," -i | grep ");

		token = strtok(NULL," ");
		while(token != NULL) {
			strcat(command,token);
			strcat(command," -i | grep ");
			token = strtok(NULL," ");			
		}
		strcat(command,"'GX[0-9]\\{3\\}\\-[0-9]\\{2\\}\\-[0-9]\\{7,8\\}' -o");
		char *counting = new char[s.size()+460];
		strcpy(counting,command);	//for finding the no of output documents
		strcat(counting," -c");
		FILE *fp2 = popen(counting,"r");
		fscanf(fp2,"%s",cc);
		fclose(fp2);	//no of matches

		strcat(command," | ./");
		strcat(command,presenter);strcat(command," ");
		strcat(command,ide);strcat(command," ");
		strcat(command,cc);		//final command
		strcat(command," >> ");
		strcat(command,results);
		start = clock();
		system(command);
		end = clock();
		double dur = (double)(end-start)/CLOCKS_PER_SEC;
		A[id] = dur;
		B[id] = stoi(cc);
		tot += B[id];
		delete[] input,command,counting;
	}
	hasher(output,A,B);
	return 0;	
}
