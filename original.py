import re
import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')
import string
import heapq

#def train():
def main():
	TRAINING = open("output.txt", encoding="cp437")
	line = TRAINING.readline()

	data = []
	sentences = {}

	while line:
		data.append(line)
		line = TRAINING.readline()
	
	frequency = {}
	for i in data:
		clean = i.replace(r'^\s+|\s+?$','')
		clean = clean.replace('\n',' ')
		clean = clean.replace("\\",'')
		clean = clean.replace(",",'')
		clean = clean.replace('"','')
		clean = re.sub(r'\[[0-9]*\]','',clean)

		sentences[i] = sent_tokenize(clean)
		frequency[i] = {}

		clean = clean.lower()
		for word in word_tokenize(clean):
			if word not in stop_word and word not in string.punctuation:
				if word not in frequency[i]:
					frequency[i][word]=1
				else:
					frequency[i][word]+=1

		max_fre = max(frequency[i].values())
		for word in frequency[i]:
			frequency[i][word]=(frequency[i][word]/max_fre)

#----------------------------------------------------------------

#def generateSum(sentences):

	sentence_score = {}
	final = {}
	for i in frequency:
		sentence_score[i] = {}
		final[i] = {}
		for sent in sentences[i]:
		    for word in word_tokenize(sent):
		    	if word in frequency[i]:
		    		if len(sent.split(' '))<30:
		    			if sent not in sentence_score.keys():
		    				sentence_score[i][sent] = frequency[i][word]
		    			else:
		    				sentence_score[i][sent]+=frequency[i][word]


		summary = heapq.nlargest(10, sentence_score[i], key = sentence_score[i].get)
		summary = ' '.join(summary)
		final[i] = "SUMMARY:\n " + summary

		print(final[i])

#----------------------------------------------------------------

main()
