import os	#for iterating over all files in a directory
import nltk	#for stem/lemmatisation and tokenization of words
import io
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
import threading
path = 'alldocs/'
queries = 'query.txt'
output = 'output.txt'
inv_index = {}
l = 6377	#no of documents
#to tokenize a string s , we do word_tokenize(s) which returns a list of tokens
#to lemmatize a word w , we can use SnowBall stemmer in english as follows
#stemmer = SnowballStemmer("english")
#stemmer.stem(w) outputs stemmatized version of the string

stemmer = SnowballStemmer("english")

def search(result,qid,query,postlist):
	query = query.split()
	query = nltk.word_tokenize(query)
	query = [stemmer.stem(word) for word in query]
	terms = [query[0]]
	final = postlist[query[0]]
	if(len(query) > 1) :
		i = 0							#td : check when len = 1
		while i < (len(query)-1):
			i += 1		
			temp = []
			if(query[i] in terms) :
				i += 1
				continue
			else :
				terms.append(query[i])
			sep = postlist[query[i]]
			x,y = sep,final
			if(len(final) < len(sep)) :
				x,y = final,sep
			for w in x :
				if w in y:
					temp.append(w)
			if(len(temp) == 0) :
				return
			final = temp
	result[qid] = final
	return

files = os.listdir(path)
def executef(lockf,locki):
	global files,inv_index,path,stemmer,l
	while True:
		lockf.acquire()
		fileo = files.pop()
		i = len(files)
		lockf.release()
		if i==0 :
			return
		if (l-i)%10==0 :
			print "Indexed upto %d files\n"%(l-i)
		fileorg = fileo
		fileo = path + fileo
		doc = io.open(fileo,'r',encoding = 'utf-8')
		temp = []
		for line in doc:
			tokens = nltk.word_tokenize(line[:-1])
			locki.acquire()
			for word in tokens:
				if word in temp: 
					continue
				else :
					temp.append(word)
				word = stemmer.stem(word)
				
				if(word in inv_index.keys()):
					inv_index[word].append(fileorg)
				else :
					inv_index[word] = [fileorg]
			locki.release()
		doc.close()

'''	
i=0
for filename in files:
	fileorg = filename
	filename = path + filename
	doc = io.open(filename,'r',encoding = 'utf-8')
	temp = []
	for line in doc:
		tokens = nltk.word_tokenize(line[:-1])
		for word in tokens:
			if word in temp: 
				continue
			else :
				temp.append(word)
			word = stemmer.stem(word)
			if(word in inv_index.keys()):
				inv_index[word].append(fileorg)
			else :
				inv_index[word] = [fileorg]
			
	doc.close()
	i += 1
	if i%10==0 :
		print "Indexed upto %d files\n"%(i)'''
results = {}
timing = {}
rel = {}
def maintask():
	global results,timing,stemmer,rel,inv_index,path,queries,output
	
	
	#creating a lock for files
	lockf = threading.Lock()
	#creating a lock for index
	locki = threading.Lock()

	#starting two threads
	t1 = threading.Thread(target=executef,args=(lockf,locki,))
	t2 = threading.Thread(target=executef,args=(lockf,locki,))		

	#starting the threads
	t1.start()
	t2.start()
	
	#waiting for their operation to complete
	t1.join()
	t2.join()	
		
	query = open(queries,'rU')
	print("indexing completed")
	for line in query:
		words = line.split('\n')
		words = words[0]
		one,two = words[:3],words[5:]
		one = int(one)
		results[one] = []
		start = datetime.now()
		search(results,one,two,inv_index)	#function for searching the documents in the inverted postings index
		timing[one] = datetime.now() - start
		break
	query.close()

	print "Hello , bye"
	print results[701]

	benchm = open(output,'rU')
	for line in benchm:
		words = line.split('\n')
		words = words[0]
		one,two = words[:3],words[4:]
		one = int(one)
		if one not in rel.keys():
			rel[one] = 0
		if one in results.keys():
			if two in results[one]:
				rel[one] += 1
		break
	benchm.close()
	print(rel[701])
	print("Searches Complete")
	print "Query ID 	Timing		Precision(%c) 		   Recall(%c)"%('%','%')
	for id in results.keys():
		r = rel[id]/50.0
		r *= 100
		if rel[id] != 0:
			p = float(rel[id])/len(results[id])
		else:
			p = 0.0
		p *= 100
		print "%d     	%d.%d		%f 		   %f"%(id,timing[id].seconds,timing[id].microseconds,p,r)
		break



if __name__ == "__main__":
	maintask()



