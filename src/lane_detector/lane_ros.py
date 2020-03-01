#!/usr/bin/env python3
import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from autonet_r1.msg import LaneRes
from reg_line1_oneL import RegLine
bridge = CvBridge()

image_pub = rospy.Publisher("/lane/debug_img",Image)
res_pub = rospy.Publisher("/lane/res",LaneRes)

rl = RegLine()

def img_clb(data):
    # global bridge
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    out_img = cv_image.copy()
    # cv2.imshow("Image window", cv_image)
    # cv2.waitKey(3)
    e1, e2, out_img = rl.reg_line(cv_image, show=True)
    lr_msg = LaneRes()
    # lr_msg.color = str(color)
    lr_msg.e1 = e1
    lr_msg.e2 = e2
    # lr.e1 = 
    res_pub.publish(lr_msg)
    image_pub.publish(bridge.cv2_to_imgmsg(out_img, "bgr8"))
    


image_sub = rospy.Subscriber(
    "/camera1/image_raw/throttled", Image, img_clb)

# ic = image_converter()
rospy.init_node('image_converter', anonymous=True)

try:
    rospy.spin()
except KeyboardInterrupt:
    print("Shutting down")
# cv2.destroyAllWindows()
