import nltk,io,string,os,sys
import collections		#for ordered dictionaries
from nltk.stem import PorterStemmer
from collections import defaultdict
'''
using rocchio's algorithm to update query vectors
Q_updated = Q_pres + B*centroid_of_top_10_relevant_documents
B = 0.65
'''

docs_opened = defaultdict(lambda : 0)
docs_present = defaultdict(lambda : 0)
doc_vectors = {}
query_vec = {}

output = 'output.txt'
query_vecs = 'query_vectors.txt'
doc_vectorf = 'doc_vectors/'
u_queryf = 'updated_query.txt'
uspace = ' '
newline = '\n'
uspace = unicode(uspace)
newline = unicode(newline)
B = 0.065		#B= beta * 1/10 = 0.65 * 0.1

def documentvec(docid,tempvec):
	doc = io.open(doc_vectorf+docid,'r',encoding='utf-8')
	full = doc.read().strip().split()
	for word in full:
		tempvec[word] += 1
	doc.close()
	doc_vectors[docid] = tempvec

files = os.listdir(doc_vectorf)
for file in files:
	docs_present[file] += 1

doc = io.open(query_vecs,'r',encoding='utf-8')
outp = io.open(output,'r',encoding='utf-8')
full = doc.read().strip().split('\n')
full2 = outp.read().strip().split('\n')
doc.close()
outp.close()
for lines in full:	#for each query vector in the query_vector file ,construct the query vector,find the top 10 relavent documents and construct their relavent vectors and update the query vector
	line = lines.split()
	id = int(line[0])	#query number
	temp = defaultdict(lambda : 0.0)
	i , count = 1 , len(line)
	while i < count:
		temp[line[i]] = int(line[i+1])
		i += 2
	query_vec[id] = temp 	#preparing the query vector
	i = 50*(id-701)			#starting id of query in the output.txt
	centroid = defaultdict(lambda : 0)
	j , limit = 0 , 10
	while j < limit and limit < 50:
		docid = (full2[i+j].strip().split())[1]
		if docs_present[docid]==0:
			limit += 1
			j += 1
			continue
		if docs_opened[docid] == 0:
			tempvec = defaultdict(lambda : 0)
			documentvec(docid,tempvec)
			docs_opened[docid] += 1
		for word in doc_vectors[docid].keys():
			centroid[word] += doc_vectors[docid][word]
		j += 1
	for word in centroid.keys():
			temp[word] += B*centroid[word]
out = io.open(u_queryf,'w')
for id in sorted(query_vec.keys()):
	vec = query_vec[id]
	out.write(unicode(id))
	out.write(uspace)
	for word in vec.keys():
		out.write(word+uspace+str(vec[word])+uspace)
	out.write(newline)
out.close()