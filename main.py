import os
import pickle
import sys

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

def goright(lst, index, pos):
    p = index
    length = len(lst)

    while p < (length - 1):
        if lst[p][pos] == lst[p + 1][pos]:
            p += 1
        else:
            break
    return p

def goleft(lst, index, pos):
    p = index
    while p > 0:
        if lst[p][pos] == lst[p - 1][pos]:
            p += -1
        else:
            break
    return p

def getComment(commentList, profname):
    index = binarySearch(profname, commentList)
    left = goleft(commentList, index, 0)
    right = goright(commentList, index, 0)
    return commentList[left:right + 1]


def stemAnalyzeData(profList, commentList, stemList, name):
    
    for prof in profList:
        comments = getComment(commentList, prof[0])
        string = ''
        for comment in comments:
            string += comment[1] + ' '
        lst = sentenceSplit(string)
        length = len(comments)
        m1 = findMatch(lst, ['smart', 'brilliant', 'knowledgeable']) / length
        m2 = findMatch(lst, ['hard', 'difficult', 'challenging']) / length
        m3 = findMatch(lst, ['funny', 'hilarious', 'entertaining']) / length
        field = ''
        if determineSTEM(prof[1], stemList) == 0:
            field = 'stem'
        else:
            field = 'non-stem'
        line = name + '|' + prof[0] + '|' + prof[1] + '|' + field + '|' + \
               str(prof[2]) + '|' + prof[4] + '|' + str(m1) + '|' + \
               str(m2) + '|' + str(m3) + '\n'
        m.write(line)

stemList = ['Psychology', 'Biology', 'Chemistry','Physics', 'Computer Science', 'Mathematics', 
'Science', 'Neuropsychiatry', 'Physics & Astronomy', 'Statistics', 
'Mathematics & Statistics', 
'Physics  Astronomy', 'Medicine', 'Engineering', 'Biological Sciences', 
'Biochemistry', 'Astronomy', 'Botany', 'Cognitive Science', 'Neuroscience']

fileList = os.listdir(os.curdir + os.sep + 'data')
fileList.sort()
fileList = fileList[1:]

m = open('merge.txt', 'w', encoding = "utf-8")

for i in range(0, len(fileList), 2):
    name = fileList[i][:-8]
    pfile = os.curdir + os.sep + 'data' + os.sep + name + '_prof'
    cfile = os.curdir + os.sep + 'data' + os.sep + name + '_comment'
    p = open(pfile, 'rb')
    c = open(cfile, 'rb')
    profList = pickle.load(p)
    commentList = pickle.load(c)
    collegename = ' '.join(name.split('_'))
    #print('{0:^67}'.format(' '.join(name.split('_'))))
    #print()
    stemAnalyzeData(profList, commentList, stemList, collegename)
    #print()
    #print()
    #print()
m.close()


