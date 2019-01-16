import nltk,io,os
from nltk.stem import PorterStemmer
from rouge import Rouge

stemmer = PorterStemmer()

path = 'Summaries/'
ground = 'GroundTruth/Topic'
types = {'d':'Degree Centrality','l':'Text Rank'}

files = sorted(os.listdir(path))
rouge = Rouge()

print '                                  						Rouge'
print '                                      	rouge-1         rouge-2            rouge-l'
print '                                      f     p     r    f     p     r     f     p     r '

for file in files:
	candidate = io.open(path+file,'r',encoding = 'utf-8')
	hyp = candidate.read().encode('ascii').replace("\t"," ").replace("\n"," ")
	ver = file[5];
	filename = ground+ver+'.1'
	reference = io.open(filename,'r',encoding = 'utf-8')
	ref = reference.read().encode('ascii').replace("\t"," ").replace("\n"," ")
	ref = [stemmer.stem(word.lower()) for word in ref]
	ref = ''
	for word in ref:
		ref += (word+" ")
	threshold = '0.'+file[7]
	print threshold	
	ranking = types[file[8]]
	score = rouge.get_scores(hyp,ref)
	scores = score[0]
	print 'Topic '+ver+' threshold-'+threshold+' '+ranking+'          '+str(scores["rouge-1"]["f"])+'   '+str(scores["rouge-1"]["p"])+'   '+str(scores["rouge-1"]["r"])+'   '+str(scores["rouge-2"]["f"])+'   '+str(scores["rouge-2"]["p"])+'   '+str(scores["rouge-2"]["r"])+'   '+str(scores["rouge-l"]["f"])+'   '+str(scores["rouge-l"]["p"])+'   '+str(scores["rouge-l"]["r"])
	#print scores
	candidate.close()
	reference.close()
