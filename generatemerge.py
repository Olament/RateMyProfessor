import os
import pickle
import csv

def binarySearch(name, profList):
    lower = 0
    upper = len(profList) - 1

    while lower <= upper:
        middle = int(lower + (upper - lower) / 2)
        middleName = profList[middle][0]
        if middleName == name:
            return middle
        elif middleName > name:
            upper = middle - 1
        else:
            lower = middle + 1
    return -1

fileList = os.listdir(os.curdir + os.sep + 'data')
fileList.sort()
fileList = fileList[1:]

stemList = ['Psychology', 'Biology', 'Chemistry','Physics', 'Computer Science', 
'Mathematics', 'Science', 'Neuropsychiatry', 'Physics & Astronomy', 'Statistics', 
'Mathematics & Statistics', 
'Physics  Astronomy', 'Medicine', 'Engineering', 'Biological Sciences', 
'Biochemistry', 'Astronomy', 'Botany', 'Cognitive Science', 'Neuroscience']

def determineSTEM(major, stemList):
    if major in stemList:
        return 'stem'
    else:
        return 'non-stem'
    return -1

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

def findMatch(lst, vocabList):
    counter = 0
    for word in lst:
        if word in vocabList:
            counter += 1
    return counter

m = open('merge.txt', 'w', encoding = "utf-8")
for i in range(0, len(fileList), 2):
    name = fileList[i][:-8]
    schoolname = ' '.join(name.split('_'))
    cfile = os.curdir + os.sep + 'rawdata' + os.sep + name + '_comment'
    pfile = os.curdir + os.sep + 'rawdata' + os.sep + name + '_prof'
    c = open(cfile, 'rb')
    p = open(pfile, 'rb')
    commentList = pickle.load(c)
    profList = pickle.load(p)
    for comment in commentList:
        prof = profList[binarySearch(comment[0], profList)]
        stem = determineSTEM(prof[1], stemList)
        split = sentenceSplit(comment[1])
        match1 = findMatch(split, ['smart', 'brilliant', 'knowledgeable'])
        match2 = findMatch(split, ['hard', 'difficult', 'challenging'])
        match3 = findMatch(split, ['funny', 'hilarious', 'entertaining'])
        line = schoolname + '|' + prof[0] + '|' + prof[1] + '|' + stem + \
        '|' + str(prof[2]) +'|' + prof[4] + '|' + \
        str(match1) + '|' + str(match2) + '|' + str(match3) + '|' + \
        str(len(split)) + '|' + \
        comment[1].replace('\n', ' ').replace('\r', '') + '\n'
        m.write(line)
m.close()


