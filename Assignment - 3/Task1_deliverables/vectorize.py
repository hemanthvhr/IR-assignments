import nltk,io,string,os,sys
import collections		#for ordered dictionaries
from nltk.stem import PorterStemmer
from collections import defaultdict

stemmer = PorterStemmer()

queryf = 'query.txt'
query_vecf = 'query_vectors.txt'
doc_vectorf = 'doc_vectors/'
path = 'alldocs/'
uspace = ' '
newline = '\n'
uspace = unicode(uspace)
newline = unicode(newline)
'''
We will be using lnf form of tf-idf vectors for both query and docs and
also the vector will be stored as follows -
for a query - 'state supports state and centre relation'
the vector will be - {'and':1,'centre':1,'relation':1,'state':2,'supports':1}
to avoid wastage of space storing tf of all words in the corpus

And for each document doc-xx in the alldocs corpus , its tf-idf vector will be stored in doc-xx in the doc_vectors folder
'''

#for finding vectors of the queries
doc = io.open(queryf,'r',encoding='utf-8')
out = io.open(query_vecf,"w")
full = doc.read().strip().split('\n')
doc.close()
for lines in full:
	temp = defaultdict(lambda : 0)
	line = lines.split()
	id = int(line[0])
	for word in line[1:]:
		temp[stemmer.stem(word)] += 1
	#then print to the query_vector file
	out.write(unicode(id))
	out.write(uspace)
	for word in temp.keys():
		out.write(word+uspace+str(temp[word])+uspace)
	out.write(newline)
	del temp
out.close()

files = os.listdir(path)
for c,file in enumerate(files):
	doc = io.open(path+file,'r',encoding='utf-8')
	full = nltk.word_tokenize(doc.read().strip())
	doc.close()
	temp = defaultdict(lambda : 0)
	for word in full:
		#print(file +' ' +word+' ') 
		temp[stemmer.stem(word)] += 1
	#then print it to the doc_vector folder
	out = io.open(doc_vectorf+file,'w')
	for word in temp.keys():
		out.write(word+uspace+str(temp[word])+uspace)
	out.close()
	del temp
	if c%100==0 :
		print 'No of Docs - ',c

