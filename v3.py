import re
import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')
import string
import heapq
import math

#def train():
def main():
	TRAINING = open("output.txt", encoding="cp437")
	DWORDS = open("terms.txt", encoding="cp437")
	OUT = open('C:/Users/Emma/Desktop/nlp/final/outputSumm.txt', 'w', newline='\n', encoding="cp437")
	line = TRAINING.readline()
	data = []
	sentences = {}
	count = 0
	d_words = []
	bad = ["do", "did", "that", "that\'s", "I", "am", "what", "which"]

	dline = DWORDS.readline()
	while dline:
		d_words.append(dline)
		dline = DWORDS.readline()

	while line:
		data.append(line)
		line = TRAINING.readline()

	frequency = {}
	tfidf = {}
	for i in data:
		clean = i.replace(r'^\s+|\s+?$','')
		clean = clean.replace('\n',' ')
		clean = clean.replace("\\",'')
		clean = clean.replace(",",'')
		clean = clean.replace('"','')
		clean = re.sub(r'\[[0-9]*\]','',clean)

		sentences[i] = sent_tokenize(clean)
		frequency[i] = {}
		tfidf[i] = {}

		count += 1
		clean = clean.lower()
		for w in word_tokenize(i):
			temp = []
			temp = w.split(".")
			for word in temp:
				if word not in stop_word and word not in string.punctuation and word not in bad:
					if word not in frequency[i]:
						frequency[i][word] = [1, 1, count] #word freq, doc freq, most recent doc
					else:
						frequency[i][word][0] += 1
						if count != frequency[i][word][2]:
							frequency[i][word][1] += 1
							frequency[i][word][2] = count

		for word in frequency[i]:
			tfidf[i][word] = frequency[i][word][0] * math.log(count/frequency[i][word][1], 10)
			if word in d_words:
				tfidf[i][word] *= 2

#----------------------------------------------------------------

#def generateSum(sentences):
	sentence_score = {}
	final = {}
	for i in frequency:
		sentence_score[i] = {}
		final[i] = {}
		for sent in sentences[i]:
		    for word in word_tokenize(sent):
		    	if word in frequency[i] and len(sent.split(' '))<30 and len(sent.split(' '))>3:
	    			if sent not in sentence_score.keys():
	    				sentence_score[i][sent] = frequency[i][word]
	    			else:
	    				sentence_score[i][sent]+=frequency[i][word]

		summary = heapq.nlargest(10, sentence_score[i], key = sentence_score[i].get)
		summary = ' '.join(summary)
		final[i] = "SUMMARY:\n " + summary

		OUT.write(final[i] + "\n")

#----------------------------------------------------------------

main()
