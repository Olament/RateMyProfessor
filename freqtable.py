from nltk.corpus import wordnet as wn
import pickle
import os
from collections import Counter

def cleanString(string):
    lst = []
    for char in string:
        if char.isalpha():
            lst.append(char.lower())
    return ''.join(lst)

def sentenceSplit(string):
    lst = string.split()
    for i in range(0, len(lst)):
        lst[i] = cleanString(lst[i])
    return lst

adj = {x.name().split('.', 1)[0] for x in wn.all_synsets('a')}
adjList = []

fileList = os.listdir(os.curdir + os.sep + 'data')
fileList.sort()
fileList = fileList[1:]

for i in range(0, len(fileList), 2):
    name = fileList[i][:-8]
    cfile = os.curdir + os.sep + 'data' + os.sep + name + '_comment'
    c = open(cfile, 'rb')
    commentList = pickle.load(c)
    for comment in commentList:
        wordLits = sentenceSplit(comment[1])
        for word in wordLits:
            if word in adj:
                adjList.append(word)

counts = Counter(adjList).most_common(200)

print('beautiful' in adjList)


