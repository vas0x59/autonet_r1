#!/usr/bin/env python3
import rospy
import tf
import tf2_ros


from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int16, Bool
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
from autonet_r1.srv import SetOdom, SetOdomResponse
from autonet_r1.src.tools.tf_tools import *
import math

# from Motor2 import Motor
from Odometry_calc import OdometryCalc
import json
# from PID import PID


rospy.init_node('motor2_ros', anonymous=True)
config_path = rospy.get_param("~config")
config = json.load(open(config_path))
print(config)
robot_W = config["robot_W"]
wheel_d = config["wheel_d"]
update_rate = config["update_rate"]
frame_name = config["frame_name"]
# kp = config["motor_v_pid"]["p"]
# ki = config["motor_v_pid"]["i"]
# kd = config["motor_v_pid"]["d"]

# m1 = Motor(n=1, d=wheel_d)S
# m2 = Motor(n=2, d=wheel_d)
# m1_pid = PID(kp, ki, kd)
# m2_pid = PID(kp, ki, kd)

odom_pub = rospy.Publisher('odom', Odometry, queue_size=50)
odom_broadcaster = tf.TransformBroadcaster()

# encoder1 = rospy.Subscriber('/encoder1', Float32, queue_size=10)
# encoder2 = rospy.Publisher('/encoder2', Float32, queue_size=10)

motor1 = rospy.Publisher('/motor1', Float32, queue_size=10)
motor2 = rospy.Publisher('/motor2', Float32, queue_size=10)
# first_enc_m1 = None
# first_enc_m2 = 0

odometry_c = OdometryCalc(w=robot_W)

# m1_target_v = 0
# m2_target_v = 0
target_x_v = 0
target_a_z_v = 0
cm1 = 0
cm2 = 0
# m1_v = 0
# m2_v = 0
cmd_vel_status = True



def m1tv_clb(data):
    global cm1
    cm1 = data.data


def m2tv_clb(data):
    global cm2
    cm2 = data.data


def set_odom(data):
    global odometry_c
    odometry_c.set(data.x, data.y, data.yaw)
    return SetOdomResponse()
def cmd_vel_clb(data: Twist):
    global target_x_v, target_a_z_v
    target_x_v = data.linear.x
    target_a_z_v = data.angular.z
    
    

rospy.Subscriber("/encoder1", Float32, m1tv_clb)
rospy.Subscriber("/encoder2", Float32, m2tv_clb)
rospy.Subscriber("/cmd_vel", Twist, cmd_vel_clb)
# rospy.Subscriber("/yaw_speed", Float32, m2tv_clb)
set_odom_srv = rospy.Service('set_odom', SetOdom, set_odom)
# rospy.Subscriber("/set_odom", Bool, set_odom())
# rospy.Subscriber("/navigate", Pose, m1tv_clb)


# tf2.

def control_motors():
    global m1_target_v, m2_target_v, m1, m2, m1_pid, m2_pid, target_a_z_v, target_x_v, robot_W
    # print("motor_target", m1_target_v - m1.get_v_ms(), m2_target_v - m2.get_v_ms())
    if cmd_vel_status == True:
        m1_target_v = target_x_v + target_a_z_v*robot_W*2
        m2_target_v = target_x_v - target_a_z_v*robot_W*2
    motor1.publish(m1_target_v)
    motor2.publish(m2_target_v)


last_time = rospy.Time.now()
prev_m1_m = 0
prev_m2_m = 0
i = 0
first_t = True


def calc_odometry():
    global first_t, odom_broadcaster, motor1, motor2, odom_pub, last_time, prev_m1_m, prev_m2_m, i, cm1, cm2
    # if first_enc_m1 is None:
    #     first_enc_m1 = m1.get_m()
    #     first_enc_m2 = m2.get_m()
    # encoder1.publish(m1.get_m()-first_enc_m1)
    # encoder2.publish(m2.get_m()-first_enc_m2)
    # encoder1_v.publish(m1.get_v_ms())
    # encoder2_v.publish(m2.get_v_ms())
    if not first_t:
        i = 0
        # cm1 = m1.get_m()-first_enc_m1
        # cm2 = m2.get_m()-first_enc_m2
        current_time = rospy.Time.now()
        x, y, th, vx, vy, vth = odometry_c.calc((current_time - last_time).nsecs/1000/1000/1000,
                                                cm1-prev_m1_m,  cm2-prev_m2_m)
        # x = -x
        # print(round(cm1 - prev_m1_m, 3), round(cm2 - prev_m2_m, 3),
        #   "xy", round(x, 3), round(y, 3), "th", th)
        prev_m1_m = cm1
        prev_m2_m = cm2

        odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
        # odom_broadcaster.sendTransform()
        odom_broadcaster.sendTransform(
            (x, y, 0.),
            odom_quat,
            current_time,
            "base_link",
            "odom")

        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"

        # set the position
        odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

        # set the velocity
        odom.child_frame_id = "base_link"
        odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

        # publish the message
        odom_pub.publish(odom)
        last_time = current_time
    i += 1
    first_t = False


def do():
    control_motors()
    calc_odometry()


    # pass
print("BBBBBBBBBBBB")
rospy.sleep(1)
print("AAAAAAAAAAAAAAAAAAAA")
# odometry_c.set()
r = rospy.Rate(update_rate)  # 10hz
while not rospy.is_shutdown():
    do()
    r.sleep()

# rospy.
# odometry_c.calc()


# def calc_odometry():
#     # global robot_W
#     O(t+1)  = O(t) + (Dr - Dl)/W
