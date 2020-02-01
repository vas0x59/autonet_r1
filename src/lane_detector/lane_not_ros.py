#!/usr/bin/env python3


import cv2
from reg_line1_oneL import RegLine

rl = RegLine()

cap = cv2.VideoCapture(2)

while True:
    ret, img = cap.read()
    e1, e2, out_img = rl.reg_line(img, show=True)
    # cv2.imshow("img", img)
    if cv2.waitKey(1)==27:    # Esc key to stop
        break
    
cap.release()
cv2.destroyAllWindows()
