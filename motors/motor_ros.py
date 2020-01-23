from Motor import Motor
from nav_msgs.msg import Odometry
from Odometry_calc import OdometryCalc
import json
config = json.load(open("config.json"))

robot_W = config["W"]

m1 = Motor(n=1, d=0.07)
m2 = Motor(n=1, d=0.07)


odometry = rospy.Publisher('odometry', Odometry, queue_size=10)
rospy.init_node('motor_ros', anonymous=True)

odometry_c = OdometryCalc(w=robot_W)



# def calc_odometry():
#     # global robot_W
#     O(t+1)  = O(t) + (Dr - Dl)/W