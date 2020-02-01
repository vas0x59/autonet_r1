#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import Int16



cmd = ""
rospy.init_node("graber", anonymous=True)
pub1 = rospy.Publisher("/arduino/servo1", Int16, queue_size=10)
pub2 = rospy.Publisher("/arduino/servo2", Int16, queue_size=10)
def callback(data):
    global cmd
    cmd = data.data

def take():
    pub2.publish(180)
    time.sleep(1)
    pub1.publish(180)

def throw():
    pub1.publish(0)
    time.sleep(0.5)
    pub2.publish(0)


rospy.Subscriber("/grab/cmd",Int16, callback)
# rospy.spin()
r = rospy.Rate(10)
pub1.publish(180)
r.sleep()
while not rospy.is_shutdown():
    if (cmd == 1):
        # print("take")
        take()
    if (cmd == 2):
        #print("throw")
        throw()
    r.sleep()



#export ROS_MASTER_URI=http://192.168.19.14:11311
