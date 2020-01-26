from PIL import Image
import pytesseract
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    img = np.flip(img, axis=1)
    text = pytesseract.image_to_string(img)
    cv2.imshow("image", img)
    print(text)
    if cv2.waitKey(10) == 27:
        break
cap.release()
cv2.destroyAllWindows()

