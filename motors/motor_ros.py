import rospy

from Motor import Motor
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from Odometry_calc import OdometryCalc
import json
from PID import PID
config = json.load(open("config.json"))

robot_W = config["robot_W"]
wheel_d = config["wheel_d"]
update_rate = config["update_rate"]
frame_name = config["frame_name"]
kp = config["motor_v_pid"]["p"]
ki = config["motor_v_pid"]["i"]
kd = config["motor_v_pid"]["d"]

m1 = Motor(n=1, d=wheel_d)
m2 = Motor(n=2, d=wheel_d)
m1_pid = PID(kp, ki, kd)
m2_pid = PID(kp, ki, kd)

odometry = rospy.Publisher('/odometry', Odometry, queue_size=10)


odometry_c = OdometryCalc(w=robot_W)

m1_target_v = 0
m2_target_v = 0

# m1_v = 0
# m2_v = 0


def m1tv_clb(data):
    global m1_target_v
    m1_target_v = data.data


def m2tv_clb(data):
    global m2_target_v
    m2_target_v = data.data


rospy.Subscriber("/m1_v", Float32, m1tv_clb)
rospy.Subscriber("/m2_v", Float32, m1tv_clb)

rospy.init_node('motor_ros', anonymous=True)


def control_motors():
    global m1_target_v, m2_target_v, m1, m2, m1_pid, m2_pid
    m1.set_power(m1_pid.calc(m1_target_v - m1.get_v_ms()))
    m2.set_power(m2_pid.calc(m2_target_v - m2.get_v_ms()))

# def 

def do():
    control_motors()
    # pass


r = rospy.Rate(update_rate)  # 10hz
while not rospy.is_shutdown():
    do()
    r.sleep()

# rospy.
# odometry_c.calc()


# def calc_odometry():
#     # global robot_W
#     O(t+1)  = O(t) + (Dr - Dl)/W
