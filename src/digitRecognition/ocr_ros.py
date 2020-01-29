#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

from OCR import NumReg

bridge = CvBridge()
nr = NumReg()

rospy.init_node('ocr', anonymous=True)

ocr_pub_text = rospy.Publisher('/ocr/addr', String, queue_size=10)
# ocr_pub_color = rospy.Publisher('/ocr/color', String, queue_size=10)


def img_clb(data):
    # global bridge
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    text, color = nr.get(cv_image)
    ocr_pub_text.publish(color[0] + test)
    # ocr_pub_color.publish(color)


image_sub = rospy.Subscriber(
    "/cam2/image_raw", Image, img_clb)
# ic = image_converter()


try:
    rospy.spin()
except KeyboardInterrupt:
    print("Shutting down")
# cv2.destroyAllWindows()
