import rospy
from std_msgs.msg import Int16
from Motor import Motor
import math


print("OK")
m1 = Motor(n=1)
m2 = Motor(n=2)   
rospy.init_node('tester_m', anonymous=True)
print("OK")
# c = 360

# d = 0.07

# k = 

d = 4
p1 = 3
def conv(c):
    return (c*p1) 

m1.set_power(10)
s = m1.enc
# rospy.sleep(2)
while m1.enc < s + (2*math.pi/1426)*7:
    rospy.sleep(0.01)
    m1.set_power(10)
m1.set_power(0)

