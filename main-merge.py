import os
import pickle
import sys
from operator import itemgetter

def getDept(profList):
    deptList = []
    for prof in profList:
        if not prof[1] in deptList:
            deptList.append(prof[1])
    deptList.sort()
    return deptList

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

def analyzeData(profList, commentList, vocabList):
    deptList = getDept(profList)
    dataList = []

    for dept in deptList:
        lst = [dept, [0, 0], [0, 0]]
        dataList.append(lst)

    #print(dataList)

    for comment in commentList:
        index = binarySearch(comment[0], profList)
        if index != -1:
            sex = profList[index][4]
            dept = profList[index][1]
            comm = sentenceSplit(comment[1])
            match = findMatch(comm, vocabList)
            lengthOfComm = len(comm)
            dataListIndex = binarySearch(dept, dataList)
            #print(dataListIndex)
            if sex == 'Male':
                dataList[dataListIndex][1][0] += match
                dataList[dataListIndex][1][1] += lengthOfComm
            else:
                dataList[dataListIndex][2][0] += match
                dataList[dataListIndex][2][1] += lengthOfComm

    maleMatchSum = 0
    maleLen = 0
    femaleMatchSum = 0
    femaleLen = 0

    for line in dataList:
        maleMatchSum += line[1][0]
        maleLen += line[1][1]
        femaleMatchSum += line[2][0]
        femaleLen += line[2][1]
        print('{0:35} {1:7} {2:7} {3:7} {4:7}'.format(line[0], line[1][0], line[1][1], line[2][0], line[2][1]))
    print('{0:35} {1:7} {2:7} {3:7} {4:7}'.format('Total', maleMatchSum, maleLen, femaleMatchSum, femaleLen))

def determineSTEM(dept, stemList):
    if dept in stemList:
        return 0
    else:
        return 1
    return -1

def stemAnalyzeData(profList, commentList, vocabList, stemList):
    dataList = [['STEM', [0, 0], [0, 0]], ['non-STEM', [0, 0], [0, 0]]]

    #print(dataList)

    for comment in commentList:
        index = binarySearch(comment[0], profList)
        if index != -1:
            sex = profList[index][4]
            dept = profList[index][1]
            comm = sentenceSplit(comment[1])
            match = findMatch(comm, vocabList)
            lengthOfComm = len(comm)
            dataListIndex = determineSTEM(dept, stemList)
            #print(dataListIndex)
            if sex == 'Male':
                dataList[dataListIndex][1][0] += match
                dataList[dataListIndex][1][1] += lengthOfComm
            else:
                dataList[dataListIndex][2][0] += match
                dataList[dataListIndex][2][1] += lengthOfComm

    maleMatchSum = 0
    maleLen = 0
    femaleMatchSum = 0
    femaleLen = 0

    for line in dataList:
        print('{0:35} {1:7.4}    {2:7.4}'.format(line[0], line[1][0] / line[1][1], line[2][0] / line[2][1]))
    #print('{0:35} {1:7} {2:7} {3:7} {4:7}'.format('Total', maleMatchSum, maleLen, femaleMatchSum, femaleLen))

stemList = ['Psychology', 'Biology', 'Chemistry','Physics', 'Computer Science', 'Mathematics', 
'Science', 'Neuropsychiatry', 'Physics & Astronomy', 'Statistics', 
'Mathematics & Statistics', 
'Physics  Astronomy', 'Medicine', 'Engineering', 'Biological Sciences', 
'Biochemistry', 'Astronomy', 'Botany', 'Cognitive Science', 'Neuroscience']

fileList = os.listdir(os.curdir + os.sep + 'data')
fileList.sort()
fileList = fileList[1:]

profList = []
commentList = []

for i in range(0, len(fileList), 2):
    name = fileList[i][:-8]
    pfile = os.curdir + os.sep + 'data' + os.sep + name + '_prof'
    cfile = os.curdir + os.sep + 'data' + os.sep + name + '_comment'
    p = open(pfile, 'rb')
    c = open(cfile, 'rb')
    subproflist = pickle.load(p)
    subcommentList = pickle.load(c)
    for prof in subproflist:
        profList.append(prof)
    for comment in subcommentList:
        commentList.append(comment)

profList.sort(key = itemgetter(0))
commentList.sort(key = itemgetter(0))


stemAnalyzeData(profList, commentList, ['smart'], stemList)

