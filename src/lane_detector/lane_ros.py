#!/usr/bin/env python3
import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
bridge = CvBridge()


def img_clb(data):
    # global bridge
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)


image_sub = rospy.Subscriber(
    "/cam1/image_raw", Image, img_clb)
# ic = image_converter()
rospy.init_node('image_converter', anonymous=True)

try:
    rospy.spin()
except KeyboardInterrupt:
    print("Shutting down")
cv2.destroyAllWindows()
