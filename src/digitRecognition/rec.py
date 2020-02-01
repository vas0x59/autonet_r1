import time
import cv2
import numpy as np

from autonet_r1.src.digitRecognition.OCR import NumReg
# from shapeDetector import shapeDetector
from autonet_r1.src.digitRecognition.colorRecognition import colorRec




class rec:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.i = 0
        self.filt = ''
        print("started")
        self.color = ""
        self.text = ""
        
        self.nr = NumReg()
        # sd = shapeDetector()
        self.cr = colorRec()
    def most_frequent(self, s): 
        return max(set(s), key = s.count) 

    def recog(self):
        
        # while cv2.waitKey(1) != ord('q'):
        _, frame = self.cap.read()
        
        # if self.i == 3:
        #     print("[DEBUG]", self.text)    
        #     self.i = 0
        #     self.filt = ''
        
        
        _, frame = self.cap.read()
        self.text = self.nr.get(frame, show = False)
        self.color = self.cr.colorRec(frame)
        print("[DEBUG]", self.color, self.text)
        # if self.text == '': return 
        # if int(self.text) > 5: return
        # self.filt += self.text
        # self.i += 1
        return self.text, self.color
