import numpy as np
import cv2

class shapeDetector:
    def __init__(self):
        self.areas = list()
    
    def detect(self, img, show = False):
        contours_approx = list()
        imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # _, thresh = cv2.threshold(imgGrey, 100, 255, cv2.THRESH_BINARY)
        thresh = cv2.adaptiveThreshold(imgGrey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 12)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # cv2.imshow("img", img)
        for contour in contours:
            if cv2.contourArea(contour) < 500: continue
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 4:
                x1 ,y1, w, h = cv2.boundingRect(approx)
                aspectRatio = float(w)/h
                self.areas.append(img[x:x+w, y1:y1+h])
                '''
                if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                    cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                else:
                    cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                '''
                contours_approx.append(approx)
        cv2.imshow("img", img)
        cv2.waitKey(1)
        return self.areas
