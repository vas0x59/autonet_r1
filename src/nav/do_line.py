#!/usr/bin/env python3

import rospy
import tf
import math
import numpy as np
import json

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
from std_msgs.msg import Float32

from autonet_r1.srv import Navigate, GetPath, SetNav, GetTelemetry, GetGrabPath
from autonet_r1.msg import LaneRes, PathNamed3, PathNamed2
from autonet_r1.src.tools.tf_tools import *
from autonet_r1.src.motors.PID import PID

E1_K = 0.5
E2_K = 0.5

PID_P = 0.03
PID_I = 0
PID_D = 0

target_speed = 0.3

lr_e1 = 0
lr_e2 = 0
lr_color = ""
rospy.init_node("do_line", anonymous=True)


def lr_clb(data):
    global lr_e1, lr_e2, lr_color
    lr_e1 = data.e1
    lr_e2 = data.e2
    lr_color = data.color


lane_res = rospy.Subscriber("/lane/res", LaneRes, lr_clb)
m1 = rospy.Publisher("/motor1", Float32, queue_size=10)
m2 = rospy.Publisher("/motor2", Float32, queue_size=10)

pid_l = PID(PID_P, PID_I, PID_D)


def calc():
    global m1, m2, lr_e1, lr_e2, lr_color, pid_l, E1_K, E2_K, target_speed
    error = (lr_e1*E1_K + lr_e2*E2_K)
    print("err", error, "e1", lr_e1, "e2", lr_e2)

    a = pid_l.calc(error - 0)
    m1.publish(float(target_speed - a))
    m2.publish(float(target_speed + a))
    


r = rospy.Rate(10)  # 10hz
while not rospy.is_shutdown():
    calc()
    r.sleep()
