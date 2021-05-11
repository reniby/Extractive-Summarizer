import re
import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')
import string
import heapq
import math
import scipy
from scipy import spatial

def main():
	TRAINING = open("output.txt", encoding="cp437")
	DWORDS = open("terms.txt", encoding="cp437")
	OUT = open('C:/Users/Emma/Desktop/nlp/final/outputSumm.txt', 'w', newline='\n', encoding="cp437")
	OUTT = open('C:/Users/Emma/Desktop/nlp/final/similarity.txt', 'w', newline='\n', encoding="cp437")
	line = TRAINING.readline()
	data = []
	sentences = {}
	count = 0
	d_words = []

	userin = []
	userin = input("Enter a list of key terms, seperated by spaces: ").split(" ")
	print(userin)
	

	dline = DWORDS.readline()
	d_words = dline.split(" ")

	count = 0
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
				if word not in stop_word and word not in string.punctuation:
					if word not in frequency[i]:
						frequency[i][word] = [1, 1, count] #word freq, doc freq, most recent doc
					else:
						frequency[i][word][0] += 1
						if count != frequency[i][word][2]:
							frequency[i][word][1] += 1
							frequency[i][word][2] = count
		
	for i in data:
		tempmax = 0
		for word in frequency[i]:
			if frequency[i][word][0] > tempmax:
				tempmax = frequency[i][word][0]
		for word in frequency[i]:
			frequency[i][word][0] = (frequency[i][word][0]/tempmax)
			tfidf[i][word] = frequency[i][word][0] * math.log(count/frequency[i][word][1], 10)
			if word in d_words:
				tfidf[i][word] *= 2

	uservec = []
	for word in userin:
		if word in tfidf[i]:
			uservec.append(tfidf[i][word])
		else:
			uservec.append(0)

	similarity = {}
	for i in data:
		for sent in sentences[i]:
			twovector = []
			for word in userin:
				if word in word_tokenize(sent):
					twovector.append(tfidf[i][word])
				else:
					twovector.append(0)

			num = 0
			oneden = 0
			twoden = 0		
			for elem in range(0, len(uservec)-1):
				num += uservec[elem] * twovector[elem]
				oneden += uservec[elem] * uservec[elem]
				twoden += twovector[elem] * twovector[elem]
			if num == 0:
				similarity[sent] = 0
			else:
				similarity[sent] = num / (math.sqrt(oneden) * math.sqrt(twoden))


	summary = heapq.nlargest(20, similarity, key = similarity.get)
	summary = ' '.join(summary)
	print("SUMMARY:\n " + summary)


main()