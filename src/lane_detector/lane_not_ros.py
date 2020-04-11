#!/usr/bin/env python3


import cv2
from reg_line1_oneL import RegLine

rl = RegLine()

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    e1, e2, cl, out_img = rl.reg_line(img, show=True)
    print(e1, e2, cl)
    # cv2.imshow("img", img)
    if cv2.waitKey(1)==27:    # Esc key to stop
        break
    
cap.release()
cv2.destroyAllWindows()
