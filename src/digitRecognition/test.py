import time
import cv2
import numpy as np

from OCR import NumReg
from shapeDetector import shapeDetector
from colorRecognition import colorRec


nr = NumReg()
sd = shapeDetector()
cr = colorRec()

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

def most_frequent(s): 
    return max(set(s), key = s.count) 


i = 0
filt = ''
print("started")

while cv2.waitKey(1) != ord('q'):
    _, frame = cap.read()
    
    if i == 3:
        print("[DEBUG]", text)    
        i = 0
        filt = ''
    
    
    _, frame = cap.read()
    text = nr.get(frame, show = False)
    color = cr.colorRec(frame)
    print("[DEBUG]", color)
    if text == '': continue
    try:
        if int(text) > 5: continue
    except:
        continue
    filt += text
    i += 1

cap.release()
cv2.destroyAllWindows()
