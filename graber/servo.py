#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import String


def main():
    station_up = 0
    station_down = 0
    cmd = ""

    def callback1(data):
        global station_up
        station_up = data.data

    def callback2(data):
        global station_down
        station_down = data.data

    def callback(data):
        global cmd
        cmd = data.data

    def take():
        pub1.publish(60)
        while (True):
            if (station_up == 1023):
                break
            pub2.publish(0)
        pub2.publish(90)

    def throw():
        while (True):
            if (station_down == 1023):
                break
            pub2.publish(180)
        pub2.publish(90)
        pub1.publish(180)

    pub1 = rospy.Publisher("arduino/servo1", Int16, queue_size=10)
    pub2 = rospy.Publisher("arduino/servo2", Int16, queue_size=10)
    rospy.Subscriber("grab/cmd", String, callback)
    rospy.Subscriber("arduino/analogin_1", Int16, callback1)
    rospy.Subscriber("arduino/analogin_2", Int16, callback2)
    rospy.spin()
    rospy.init_node("graber", anonymous=True)
    while not rospy.is_shutdown():
        sub_msg = cmd
        if (sub_msg == "take"):
            take()
        if (sub_msg == "throw"):
            throw()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
