import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Int32
import math
import time


class Motor:
    def __init__(self, n=1, d=0.07):
        self.n = n
        self.pub = rospy.Publisher(
            '/arduino/m' + str(self.n), Int16, queue_size=10)
        # self.sub =
        rospy.Subscriber('/arduino/enc' + str(self.n), Int32, self.callback)
        self.enc = 0
        self.d = d
        self.prev_enc = 0
        self.prev_t = time.time()
        self.v = 0
        self.encoder_const = 1426

    def callback(self, data):
        if self.n == 2:
            self.enc = -data.data
        else:
            self.enc = -data.data
        ds = (2*math.pi/self.encoder_const)*self.d*self.enc - \
            (2*math.pi/self.encoder_const)*self.d*self.prev_enc
        dt = time.time() - self.prev_t
        self.v = ds/dt
        self.prev_enc = self.enc

    def set_power(self, m):
        if self.n == 1:
            self.pub.publish(int(-m))
        else:
            self.pub.publish(int(m))

    def get_rad(self):
        return (2*math.pi/self.encoder_const)*self.enc

    def get_m(self):
        return (2*math.pi/self.encoder_const)*self.d*self.enc

    def reset(self):
        pass

    def get_v_ms(self):
        return self.v
