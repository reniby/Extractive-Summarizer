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

#def train():
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

#----------------------------------------------------------------
	print("part 1 finished")
#def generateSum(sentences):
	keeptrack = 0
	sentence_score = {}
	final = {}
	similarity = {}
	onevector = {}
	twovector = {}
	for i in frequency:
		keeptrack+=1
		similarity[i] = {}
		for one in range(0, len(sentences[i])-1):#len(sentences[i])-2):
			similarity[i][one] = {}
			for two in range(one+1, len(sentences[i])): #len(sentences[i])-1):
				if len(sentences[i][one].split(' '))>2 and len(sentences[i][two].split(' '))>2:
					onevector[i] = []
					twovector[i] = []
					for word in word_tokenize(sentences[i][one]):
						if word in tfidf[i]:
							onevector[i].append(tfidf[i][word])
							if word in word_tokenize(sentences[i][two]):
								twovector[i].append(tfidf[i][word])
							else:
								twovector[i].append(0)

						else:
							onevector[i].append(0)
							twovector[i].append(0)

					num = 0
					oneden = 0
					twoden = 0		
					for elem in range(0, len(onevector[i])-1):
						num += onevector[i][elem] * twovector[i][elem]
						oneden += onevector[i][elem] * onevector[i][elem]
						twoden += twovector[i][elem] * twovector[i][elem]
					if num == 0:
						similarity[i][one][two] = 0
					else:
						similarity[i][one][two] = num / (math.sqrt(oneden) * math.sqrt(twoden))

		tempmax = {}
		for m in range(0, len(similarity[i])):
			tempmax[m] = 0
			for n in range(m+1, len(similarity[i][m])+1):
				if n in similarity[i][m]:
					tempmax[m] += similarity[i][m][n]

		finalsummary = ''
		summary = heapq.nlargest(20, tempmax, key = tempmax.get)
		for o in summary:
			finalsummary += sentences[i][o] + " "
		final[i] = "SUMMARY:\n " + finalsummary
		print("done " + str(keeptrack))
		OUT.write(final[i] + "\n")
		break

#----------------------------------------------------------------

main()
