import pytesseract
import cv2
import numpy as np


class colorRecognition:
    def __init__(self):
        pass
    def get_color(self, img, show = False):
        img = cv2.resize(img, (280, 260))
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        if show:
            cv2.imshow("img", img)
        return "works"
