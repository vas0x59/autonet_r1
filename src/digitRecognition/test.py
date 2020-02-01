import time
import cv2
import numpy as np

from OCR import NumReg
from shapeDetector import shapeDetector
from colorRecognition import colorRecognition


nr = NumReg()
sd = shapeDetector()
cr = colorRecognition()


cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
def most_frequent(s): 
    return max(set(s), key = s.count) 


i = 0
filt = ''
while cv2.waitKey(1) != ord('q'):
    _, frame = cap.read()
    
    if i == 5:
        print(most_frequent(filt))
        print(filt)
        i = 0
        filt = ''
    
    _, frame = cap.read()
    text = nr.get(frame, show = False)
    cr.get_color(frame, show = True)


    if text == '': continue
    if int(text) > 5: continue
    filt += text
    i += 1
cap.release()
