import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Int32
import math
import time
from MedianArray import MedianArray

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
        self.prev_t = rospy.Time.now().nsecs/1000/1000/1000
        self.v = 0
        self.encoder_const = 1426
        self.prev_ds = 0
        self.prev_prev_v= 0
        self.filter = MedianArray(d_val=0)

    def callback(self, data):
        if self.n == 2:
            self.enc = -data.data
        else:
            self.enc = -data.data
        ds = (2*math.pi/self.encoder_const)*self.d*self.enc - \
            (2*math.pi/self.encoder_const)*self.d*self.prev_enc
        dt = rospy.Time.now().nsecs/1000/1000/1000 - self.prev_t
        
        # if abs(self.v - ds/dt) > 
        if self.v!=0 and abs(ds/dt - 0) < 0.06 and ds/dt != 0:
            pass
        else:
            self.v = ds/dt
        self.filter.update(self.v)
        # else:
        #     self.v = ds/dt
        self.prev_enc = self.enc
        self.prev_t = rospy.Time.now().nsecs/1000/1000/1000

    def set_power(self, m):
        if abs(m) > 5 and abs(m) < 70:

            if self.n == 1:
                self.pub.publish(int(-m))
            else:
                self.pub.publish(int(m))
        elif abs(m) >= 70:
            if self.n == 1:
                self.pub.publish(int(70 * ((m > 0)*2 - 1)))
            else:
                self.pub.publish(int(70 * ((m > 0)*2 - 1)))
        else:
            if self.n == 1:
                self.pub.publish(int(0))
            else:
                self.pub.publish(int(0))

    def get_rad(self):
        return (2*math.pi/self.encoder_const)*self.enc

    def get_m(self):
        return (2*math.pi/self.encoder_const)*self.d*self.enc

    def reset(self):
        pass

    def get_v_ms(self):
        return self.filter.getVal()
