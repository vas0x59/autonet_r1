import cv2
import numpy as np
from OCR import NumReg


nr = NumReg()

cap = cv2.VideoCapture(0)
while cv2.waitKey(1) != ord('q'):
    _, frame = cap.read()

    print(nr.get(frame))
cap.release()
