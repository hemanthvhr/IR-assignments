'''https://web.eecs.umich.edu/%7Emihalcea/papers/mihalcea.emnlp04.pdf'''

import nltk,io,string,os,sys
import collections		#for ordered dictionaries
from nltk.stem import PorterStemmer
from collections import defaultdict
from bs4 import BeautifulSoup as bp

stemmer = PorterStemmer()
if len(sys.argv)!=2:
	print 'Wrong arguments'
	exit(0)
version = sys.argv[1]
topic = 'Topic' + version
print topic
path = topic+ '/'
ver = ['1','2','3']
ranking = ['d','t']
wordorder = {}
sentences = []
scores = []
fullsentences = []			#	used for printing the actual sentences
lengthsent = []				# 	no of useful words in each sentence
#for implementing the Heap used in degree centrality algorithm
def max_heap(arr,i,ref):
	j = i
	if 2*i+1 < len(arr) and ref[arr[2*i+1]] > ref[arr[i]] :
		j = 2*i+1
	if 2*j+2 < len(arr) and ref[arr[2*i+2]] > ref[arr[i]] :
		j = 2*i+2
	if i!=j:
		arr[i],arr[j] = arr[j],arr[i]
		max_heap(arr,j,ref)
	return


def maxheapify(arr,ref):
	i = len(arr)-1
	while i>-1 :
		max_heap(arr,i,ref)
		i -= 1



def findscore(c,d):				#finds the cosine lnf similarity between sentences c and d
	x = sentences[c]
	y = sentences[d]
	sum = 0;
	a,b = x.keys(),y.keys()
	i,j = 0,0
	while i<len(a) and j<len(b):
		if i==len(a)-1:
			if a[i] < b[j]:
				break
		if j==len(b)-1:
			if a[i] > b[j]:
				break
		if a[i]==b[j] :
			sum += x[a[i]] * y[b[j]]
			i += 1
			j += 1
		elif a[i] > b[j] :
			j += 1
		else:
			i += 1
	return sum/((scores[c])*(scores[d]))


def degreecentrality(rank):
	arr = [i for i in range(nodes)]
	ref = []
	for i in range(nodes):
		sum = 0
		for j in range(nodes):
			sum += adjmat[i][j]
		ref.append(sum)
	maxheapify(arr,ref)
	while len(arr) :									# O(V) time
		top = arr[0]
		rank.append(top)
		for i in range(nodes):							# O(V) time
			if adjmat[i][top]==1:
				ref[i] -= 1
			adjmat[i][top] , adjmat[top][i] = 0,0
		arr[0],arr[-1] = arr[-1],arr[0]
		arr.pop()
		maxheapify(arr,ref)							   # O(log(V)) time


def textrank(score):
	min_thsd = 0.09			#	minimum change threshold for the page rank value
	d = 0.85			#   as was in the original paper on textrank
	ch_it = min_thsd + 0.002
	iterations = 0
	while ch_it - min_thsd > 0.001 and iterations < 20:
		ch_it = 0.0
		for i in range(nodes):
			old = score[i]
			score[i] = 1-d
			for j in range(nodes):
				score[i] += d*similarty[i][j]*score[j]/total[j]
			old = score[i] - old
			if ch_it < old:
				ch_it = old
		iterations += 1

files = os.listdir(path)
for file in files:	#reading all the files and generating the sentences and its corresponding vetors in fullsentences and sentences respectively
	doc = io.open(path+file,'r',encoding = 'utf-8')
	soup = bp(doc.read(),'html.parser')
	fulls = [word.string for word in (soup.find_all('p'))[1:]]
	for full in fulls:
		temp = full.encode('ascii').split('.')
		initial = len(fullsentences)
		fullsentences += temp
		sent = [x.translate(None,string.punctuation).strip() for x in temp]
		i = 0
		for line in sent:
			if line == '':
				fullsentences.pop(i+initial)
				continue
			temp = defaultdict(lambda : 0)
			j = 0
			for word in nltk.word_tokenize(line):
				temp[word.lower()] += 1
				j += 1
			lengthsent.append(j)
			x = collections.OrderedDict()
			score = 0.0
			for y in sorted(temp.keys()):
				x[y] = temp[y]
				score += temp[y]**2

			scores.append(score**0.5)	#used in calculating the similarity score
			sentences.append(x)
			x = None
			del temp
			i += 1
	doc.close()
print len(sentences)

threshold = 0.1- 0.00001
nodes = len(sentences)
adjmat = [[0 for i in range(nodes)] for j in range(nodes)]
similarty = [[0.0 for i in range(nodes)] for j in range(nodes)]
#generating the cosine similarity score martix
for i in range(nodes):
	for j in range(nodes):
		if i<j:
			continue
		sim = findscore(i,j)
		similarty[i][j],similarty[j][i] = sim,sim


total = [sum(similarty[i]) for i in range(nodes)]		# used for normalized weights
#print similarty
print '------------------------------------------------------------------------'

degree_rank = []
page_rank = []

for k in range(3):
	degree_rank = []
	#generating the adjancency matrix for the graph based on the threshold value 
	for i in range(nodes):
		for j in range(nodes):
			if i < j:
				continue
			if(similarty[i][j] > threshold):
				adjmat[i][j],adjmat[j][i] = 1 , 1
			else :
				adjmat[i][j],adjmat[j][i] = 0 , 0
	#calculating the ranks of the sentences through degree centrality
	degreecentrality(degree_rank)
	#writing results to a file
	summary = 'Summaries/'+topic+'_'+ver[k]+'d.txt'
	out = io.open(summary,"w")
	no_of_words = 0
	for i in range(nodes):
		no_of_words += lengthsent[degree_rank[i]]
		out.write(unicode(fullsentences[degree_rank[i]]).strip())
		out.write(unicode(' '))
		if no_of_words > 250:
			break
	out.close()
	print '------------------------------------------------------------------------'

	#calculating the textrank value of the sentences through textrank
	page_rank = [1.0/nodes for i in range(nodes)]
	textrank(page_rank)
	pagevalue = {}
	for i in range(nodes):
		pagevalue[page_rank[i]] = i
	#writing results to a file
	summary = 'Summaries/'+topic+'_'+ver[k]+'l.txt'
	out = io.open(summary,"w")
	no_of_words = 0
	for rank in sorted(pagevalue.keys()):
		no_of_words += lengthsent[pagevalue[rank]]
		out.write(unicode(fullsentences[pagevalue[rank]]).strip())
		out.write(unicode(' '))
		if no_of_words > 250:
			break
	out.close()
	print '------------------------------------------------------------------------'
	#print page_rank
	threshold += 0.1


