import pytesseract
import cv2
import numpy as np

class NumReg:
    def __init__(self, numbers="0123456789"):
        self.numbers = numbers
    def get(self, img):
        img = cv2.bitwise_not(img)
        text = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=' + str(self.numbers))
        color = "none"
        return text, color
