#!/usr/bin/env python3
# import sys
# sys.path.append('../../../autonet_r1')

import rospy
import tf2_ros
import tf

import math
import numpy as np
import json

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
from std_msgs.msg import Float32

from autonet_r1.srv import Forward, ForwardResponse
# from autonet_r1.src
from autonet_r1.src.motors.PID import PID
print("OKOKOK")
"""
"""


def get_dist(x1, y1, x2, y2):
    return ((x1-x2) ** 2 + (y1-y2) ** 2)**0.5


rospy.init_node('forward')
config_path = rospy.get_param("~config", "navigate_config.json")
motors_path = rospy.get_param("~motors_config", "../motors/config.json")
config = json.load(open(config_path))
motors_config = json.load(open(motors_path))
print(config)

mode = "disable"
target_stopper = True
start_x = 0
start_y = 0
start_yaw = 0
# target_yaw_speed = 0
target_speed = 0
target_id = 0
target_dist = 0
target_yaw = 0
# setpoint_yaw = 0
nav_state = "wait"

time_r = 0
# rospy.Time.now().to_sec()
r_x = 0
r_y = 0
r_yaw = 0


tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)

def nav_clb(data: PoseStamped):
    global r_x, r_y, r_yaw
    r_x = data.pose.position.x
    r_y = data.pose.position.y
    r_yaw = tf.transformations.euler_from_quaternion([
        data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w])[2]


nav_sub = rospy.Subscriber("/nav", PoseStamped, nav_clb)


def handle_forward(req: Forward):
    global mode, target_dist, target_yaw, target_speed, time_r, target_stopper, target_id, start_x, start_y, r_y, r_x, nav_state
    time_r = rospy.Time.now().to_sec()
    target_dist = req.dist
    target_yaw = req.yaw
    mode = req.mode
    target_stopper = req.stopper
    target_speed = req.speed
    nav_state = "start"
    target_id = req.id
    start_x = r_x
    start_y = r_y
    print(r_x, r_y)
    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    # return NavigateResponse(0)
    return ForwardResponse()


s = rospy.Service('forward', Forward, handle_forward)
m1 = rospy.Publisher("/motor1", Float32, queue_size=10)
m2 = rospy.Publisher("/motor2", Float32, queue_size=10)

r = rospy.Rate(config["update_rate"])  # 10hz
yaw_pid = PID(config["yaw_pid"]["p"], config["yaw_pid"]
              ["i"], config["yaw_pid"]["d"])
while not rospy.is_shutdown():
    # calc()
    if nav_state == "start":
        nav_state = "rotate"
        # yaw_pid = PID(config["yaw_pid"]["p"], config["yaw_pid"]["i"], config["yaw_pid"]["d"])
    if nav_state == "rotate":
        v = motors_config["robot_W"] * config["yaw_speed"]
        mv1 = v * (((target_yaw - r_yaw) > 0)*2-1)
        mv2 = -v * (((target_yaw - r_yaw) > 0)*2-1)
        m1.publish(float(mv1))
        m2.publish(float(mv2))
        if (abs(target_yaw - r_yaw) < config["yaw_th"]):
            if mode != "yaw":
                nav_state = "going"
                m1.publish(float(0))
                m2.publish(float(0))
                yaw_pid = PID(config["yaw_pid"]["p"], config["yaw_pid"]["i"], config["yaw_pid"]["d"])
            else:
                if target_stopper == True:
                    m1.publish(float(0))
                    m2.publish(float(0))
                nav_state = "done"
    if nav_state == "going":
        pid_r = yaw_pid.calc(target_yaw - r_yaw) * target_speed
        m1.publish(float(target_speed - pid_r))
        m2.publish(float(target_speed + pid_r))
        if abs(get_dist(r_x, r_y, start_x, start_y) - target_dist) < config["dist_th"]:
            if target_stopper == True:
                m1.publish(float(0))
                m2.publish(float(0))
            nav_state == "done"
    if nav_state == "done":
        nav_state = "wait"
    # m1.publish(float(0))
    # m2.publish(float(0))

    r.sleep()
