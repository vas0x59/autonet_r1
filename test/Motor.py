import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Int32


class Motor:
    def __init__(self, n):
        self.n = n
        self.pub = rospy.Publisher('/arduino/m' + str(self.n), Int16, queue_size=10)
        # self.sub = 
        rospy.Subscriber('/arduino/enc' + str(self.n), Int32, self.callback)
        self.enc = 0
    def callback(self, data):
        if self.n == 2:
            self.enc = -data.data
        else:
            self.enc = -data.data
    def set_power(self, m):
        if self.n == 1:
            self.pub.publish(-m)
        else:
            self.pub.publish(m)
