from cgitb import text
import cv2
import numpy as np
import face_recognition
from numpy import genfromtxt
import os

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
# print(encodeListKnown)

np.savetxt("Encodings.csv", 
           encodeListKnown,
           delimiter =", ", 
           fmt ='% s')
# my_data = genfromtxt('Encoding.csv', delimiter=',')
# print(my_data)

print('Encoding complete')