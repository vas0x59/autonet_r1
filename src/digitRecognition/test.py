import time
import cv2
import numpy as np

from OCR import NumReg
from shapeDetector import shapeDetector
from colorRecognition import colorRec


nr = NumReg()
sd = shapeDetector()
cr = colorRec()

try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

def most_frequent(s): 
    return max(set(s), key = s.count) 

print("started")

while cv2.waitKey(1) != 27:
    _, frame = cap.read()
    text = nr.get(frame, show = True)
    color = cr.colorRec(frame)
    if text == '': continue
    print("[DEBUG]", color, most_frequent(text))

cap.release()
cv2.destroyAllWindows()
