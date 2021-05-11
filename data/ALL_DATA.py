import nltk
import re
import copy
import treelib
import json
import sys
from nltk.corpus import webtext

f = open('ALL_DATA_2.json')
ALL_DATA = json.load(f)
OUT = open('C:/Users/Emma/Desktop/nlp/final/output.txt', 'w', newline='\n', encoding="cp437")

#BADOUT = open('C:/Users/Emma/Desktop/nlp/final/badOutput.txt', 'w', newline='\n', encoding="cp437")
#BADOUT.write(webtext.raw('overheard.txt'))
#OUTT = open('C:/Users/Emma/Desktop/nlp/final/outputBad.txt', 'w', newline='\n', encoding="cp437")
bad_turn=["Matthew", "Matt", "Mercer", "Marisha", "Ray", "Laura", "Baily", "Liam", "O'Brien", "Sam", "Riegel", "Travis", "Willingham", "Ashley", "Johnson", "Orion", "Acaba", "Critical", "Role", "Geek", "Sundry", "game", "voice", "players", "enjoy", "welcome", "5th", "edition", "pathfinder", "actors", "stream", "characters", "subscribers", "fedex", "sponsor", "shipped", "Comic", "charity", "Easter"]

count = 0
for i in ALL_DATA: #each episode
	#print(i)
	count += 1
	#OUT.write("DOCUMENT: " + str(count) + "\n")
	for j in ALL_DATA[i]['UTTERANCES']:
		current = ''
		current = j
		for word in bad_turn:
			if word.lower() in current.lower():
				current = ""
		if len(current.split(" ")) <4:
			current = ""
		try:
			OUT.write(current)
		except UnicodeEncodeError:
			pass
		#print(str(current) + "\n\n\n")	

	OUT.write("\n")
