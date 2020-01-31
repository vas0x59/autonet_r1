#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16

def main():
    cmd = ""
    rospy.init_node("graber", anonymous=True)
    pub1 = rospy.Publisher("/arduino/servo1", Int16, queue_size=10)
    pub2 = rospy.Publisher("/arduino/servo2", Int16, queue_size=10)
    def callback(data):
        global cmd
        cmd = data.data

    def take():
        pub2.publish(180)
        pub1.publish(180)

    def throw():
        pub1.publish(0)
        pub2.publish(0)

    
    rospy.Subscriber("/grab/cmd",Int16, callback)
    # rospy.spin()
    while not rospy.is_shutdown():
        global cmd
        if (cmd == 1):

            take()
        if (cmd == 2):

            throw()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
#export ROS_MASTER_URI=http://192.168.19.14:11311
