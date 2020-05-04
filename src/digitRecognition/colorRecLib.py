import numpy as np
import cv2 as cv
class ColorRec:
    def __init__(self):
        self.color = ''
    def getColor(self, image, height_shift = 50, width_shift = 50, show = 0):
        """
        Gets a square in the center of the image and by the hue value returns the color
        """
        cropped = image[image.shape[0]//2 - height_shift : image.shape[0]//2 + height_shift, image.shape[1]//2 - width_shift : image.shape[1]//2 + width_shift]
        hsv = cv.cvtColor(cropped, cv.COLOR_BGR2HSV)
        h,s,v = cv.split(hsv)
        h_new = np.median(h) * 2
        s_new = np.median(s)
        v_new = np.median(v)
        if v_new <= 10:
            self.color = 'black'
        elif v_new >= 245:
            self.color = 'white'
        else:
            if h_new >= 30 and h_new < 90:
                self.color = 'yellow'
            elif h_new >= 90 and h_new < 150:
                self.color = 'green'
            elif h_new >= 150 and h_new < 260:
                self.color = 'blue'
            elif h_new >= 260 and h_new < 310:
                self.color = 'magenta'
            elif h_new >= 310 or h_new < 30:
                self.color = 'red'
        if show:
            cv.imshow('cropped', cropped)
        return self.color