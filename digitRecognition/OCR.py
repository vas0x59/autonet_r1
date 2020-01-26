from PIL import Image
import pytesseract
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    #create negative
    #img = cv2.bitwise_not(img)
    #create gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    text = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    cv2.imshow("image", img)
    print(text)
    if cv2.waitKey(10) == 27:
        break
cap.release()
cv2.destroyAllWindows()
