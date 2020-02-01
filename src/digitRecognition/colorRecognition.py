import cv2
from color_recognition_api import color_histogram_feature_extraction
from color_recognition_api import knn_classifier
import os
import os.path

prediction = 'n.a.'

PATH = './training.data'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print ('training data is ready, classifier is loading...')
else:
    print ('training data is being created...')
    open('training.data', 'w')
    color_histogram_feature_extraction.training()
    print ('training data is ready, classifier is loading...')

class colorRec:
    def __init__(self):
        pass
    def colorRec(self, orig):
        height, width, c = orig.shape
        upper_left = (int(width / 5), int(height / 5))
        bottom_right = (int(width * 3 / 5), int(height * 3 / 5))
        frame = orig[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]
        color_histogram_feature_extraction.color_histogram_of_test_image(frame)
        prediction = knn_classifier.main('training.data', 'test.data')
        return prediction
