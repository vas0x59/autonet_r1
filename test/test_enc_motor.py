import rospy
from std_msgs.msg import Int16
from Motor import Motor
import math

rospy.init_node('tester_m', anonymous=True)
m1 = Motor(1)
m2 = Motor(2)

# c = 360

# d = 0.07

# k = 
p1 = 360
d = 0.07

def conv(c):
    return (c/p1) * (math.pi*d)

m1.set_power(10)
s = conv(m1.enc)
while conv(m1.enc) < s + 1:
    rospy.sleep(0.01)
m1.set_power(0)

