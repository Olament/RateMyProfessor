import requests
import json
import time
import pickle
import sys
from operator import itemgetter

def getProfList(schoolID):

        profList = []

        for page in range(1, 200):

            query = "http://www.ratemyprofessors.com/filter/professor/?department=\
            &page=" + str(page) + \
            "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=\
            schoolId&sid=" + str(schoolID)

            try:
                page = requests.get(query)
                jsonpage = json.loads(page.content)
                professorlist = jsonpage['professors']

                if len(professorlist) > 0:                    
                    for prof in professorlist:
                        line = []
                        line.append(prof['tFname'] + ' ' + prof['tLname'])
                        line.append(prof['tDept'])
                        line.append(prof['overall_rating'])
                        line.append(prof['tid'])
                        profList.append(line)
                        #print(line)
                else:
                    break
            except:
                pass

            time.sleep(0.5)

        profList.sort(key = itemgetter(0))

        return profList

def getComment(name, tid):

    commentList = []

    for page in range(1, 200):
    
        query = "http://www.ratemyprofessors.com/paginate/professors/ratings?tid="\
        + str(tid) + "&filter=&courseCode=&page=" + str(page)

        try:
            page = requests.get(query)
            jsonpage = json.loads(page.content)
            comments = jsonpage['ratings']

            if len(comments) > 0:
                for comment in comments:
                    if comment['rComments'] != 'No Comments' \
                    and comment['rComments'] != '':
                        line = []
                        line.append(name)
                        line.append(comment['rComments'])
                        commentList.append(line)
                        #print(line)
            else:
                break
        except:
            pass

        time.sleep(0.5)

    return commentList

def binarySearchProf(name, commentList):

    lower = 0
    upper = len(commentList) - 1

    while lower <= upper:
        middle = int(lower + (upper - lower) / 2)
        middleName = commentList[middle][0]
        if middleName == name:
            return middle
        elif middleName > name:
            upper = middle - 1
        else:
            lower = middle + 1

    return -1

def getLower(name, start, commentList):

    for i in range(start, 0, -1):
        if commentList[i - 1][0] != name:
            return i
    return 0

def getUpper(name, start, commentList):

    for i in range(start, len(commentList) - 1):
        if commentList[i + 1][0] != name:
            return i
    return len(commentList) - 1

def getProfComment(name, commentList):
    
    start = binarySearchProf(name, commentList)
    lower = 0
    upper = 0

    if start == -1:
        return []
    else:
        lower = getLower(name, start, commentList)
        upper = getUpper(name, start, commentList)

    return commentList[lower:upper + 1]

def cleanString(string):
    valids = []
    for char in string:
        if char.isalpha():
            valids.append(char)
    return ''.join(valids)

def determineSex(name, commentList):

    profCommentList = getProfComment(name, commentList)
    malePronouns = 0
    femalePronouns = 0

    for comment in profCommentList:
        commentInWord = comment[1].split()
        for aWord in commentInWord:
            word = cleanString(aWord)
            if word == 'he' or word == 'him' or word == 'his':
                malePronouns += 1
            if word == 'she' or word == 'her' or word == 'hers':
                femalePronouns += 1

    if malePronouns > femalePronouns:
        return 'Male'
    if femalePronouns > malePronouns:
        return 'Female'
    return 'Uncertain'
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.flush()
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total: 
        sys.stdout.flush()
        print()

def getData(schoolName, schoolID):

    profList = getProfList(schoolID)
    commentList = []
    print('** {} professor list downloaded **'.format(schoolName))

    profListlen = len(profList)
    for i in range(0, profListlen):
        for comment in getComment(profList[i][0], profList[i][3]):
            commentList.append(comment)
        printProgressBar(i, profListlen - 1, 'Download Comment: ', length = 50)
    print('** {} comment list downloaded **'.format(schoolName))

    profListwithSex = []

    for i in range(0, profListlen):
        sex = determineSex(profList[i][0], commentList)
        if sex != -1:
            line = [profList[i][0], profList[i][1], profList[i][2], profList[i][3], sex]
            profListwithSex.append(line)
        printProgressBar(i, profListlen - 1, 'Determine Sex: ', length = 50)
    print('** {} sex determination finished **'.format(schoolName))

    profListwithSexFile = str(schoolName) + '_prof'
    commentListFile = str(schoolName) + '_comment'
    p = open(profListwithSexFile, 'wb')
    c = open(commentListFile, 'wb')
    pickle.dump(profListwithSex, p)
    pickle.dump(commentList, c)
    p.close()
    c.close()
    print('** {} write data finished **'.format(schoolName))

getData(sys.argv[1], int(sys.argv[2]))
