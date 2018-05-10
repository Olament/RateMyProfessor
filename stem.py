import pickle
import os

fileList = os.listdir(os.curdir + os.sep + 'data')
fileList.sort()
fileList = fileList[1:]

deptList = []

for i in range(0, len(fileList), 2):
    name = fileList[i][:-8]
    pfile = os.curdir + os.sep + 'data' + os.sep + name + '_prof'
    p = open(pfile, 'rb')
    profList = pickle.load(p)
    for prof in profList:
        if not prof[1] in deptList:
            deptList.append(prof[1])

print(deptList)



['Psychology', 'Biology', 'Chemistry','Physics', 'Computer Science', 'Mathematics', 
'Science', 'Neuropsychiatry', 'Physics & Astronomy', 'Statistics', 
'Mathematics & Statistics', 
'Physics  Astronomy', 'Medicine', 'Engineering', 'Biological Sciences', 
'Biochemistry', 'Astronomy', 'Botany', 'Cognitive Science', 'Neuroscience']


