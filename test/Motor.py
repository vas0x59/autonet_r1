import rospy
from std_msgs.msg import Int16


class Motor:
    def __init__(self, n):
        self.n = n
        self.pub = rospy.Publisher('arduino/m' + str(self.n), Int16, queue_size=10)
        # self.sub = 
        rospy.Subscriber('arduino/enc' + str(self.n), Int16, self.callback)
        self.enc = 0
    def callback(self, data):
        self.enc = data.data
    def set_power(self, m):
        self.pub.publish(m)
