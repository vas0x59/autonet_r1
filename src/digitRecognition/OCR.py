import pytesseract
import cv2
import numpy as np

class NumReg:
    def __init__(self, numbers="0123456789"):
        self.numbers = numbers
    def get(self, img, show = False, inv = True):
        img = cv2.resize(img, (280, 260))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        if inv:
            img = cv2.bitwise_not(img)
        if show:
            cv2.imshow("img", img)
        text = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=' + str(self.numbers))
        return text
