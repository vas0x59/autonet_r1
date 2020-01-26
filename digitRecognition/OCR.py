import pytesseract
import cv2
import numpy as np

class recog:
    def __init__(self, cam):
        self.cap = cv2.VideoCapture(cam)
        self.text = ""
    def get(self):
        ret, img = self.cap.read()
        img = cv2.bitwise_not(img)
        text = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        return text
