#!/usr/bin/env python3
# import sys
# # sys.path.append('../../../autonet_r1')
# print(sys.path)
import rospy
import tf2_ros
import tf
import math
import numpy as np
import json

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
from std_msgs.msg import Float32

from autonet_r1.srv import Navigate, NavigateResponse
from autonet_r1.src.motors.PID import PID
from autonet_r1.src.tools.tf_tools import *
TRANSFORM_TIMEOUT = 1
LOCAL_FRAME = "nav"
"""
"""


rospy.init_node('navigate')
config_path = rospy.get_param("~config", "navigate_config.json")
motors_path = rospy.get_param("~motors_config", "../motors/config.json")
config = json.load(open(config_path))
motors_config = json.load(open(motors_path))
print(config)

mode = "disable"
target_stopper = True
target_x = 0
target_y = 0
target_yaw = 0
# target_yaw_speed = 0
target_speed = 0
target_id = 0
target_frame = "map"
# setpoint_yaw = 0
nav_state = "wait"

time_r = 0
# rospy.Time.now().to_sec()
r_x = 0
r_y = 0
r_yaw = 0


# tf_buffer = tf.Buffer()
tf_listener = tf.TransformListener()

# tf_buffer.


def nav_clb(data: PoseStamped):
    global r_x, r_y, r_yaw
    # data.pose.position
    r_x = data.pose.position.x
    r_y = data.pose.position.y
    r_yaw = tf.transformations.euler_from_quaternion([
        data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w])[2]


nav_sub = rospy.Subscriber("/nav", PoseStamped, nav_clb)

start_yaw = 0


def handle_navigate(req: Navigate):
    global mode, target_x, target_y, target_yaw, target_speed, time_r, target_stopper, target_id, nav_state, target_frame, tf_listener
    time_r = rospy.Time.now().to_sec()
    # target_x = req.x
    # target_y = req.y
    # target_yaw = req.yaw
    mode = req.mode
    target_stopper = req.stopper
    target_speed = req.speed
    nav_state = "start"
    target_id = req.id
    target_frame = req.frame
    # p = PoseStamped()
    # p.header.frame_id = req.frame
    # p.pose.position.x = req.x
    # p.pose.position.y = req.y
    # p.pose.orientation = orientation_from_euler(0, 0, req.yaw)
    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    # pose_local = tf_buffer.transform(p, LOCAL_FRAME, TRANSFORM_TIMEOUT)
    target_x, target_y, target_yaw  = transform_xy_yaw(
        req.x, req.y, req.yaw, req.frame, LOCAL_FRAME, tf_listener)
    # target_x = pose_local.pose.position.x
    # target_y = pose_local.pose.position.y
    # target_yaw = euler_from_orientation(pose_local.orientation)[2]
    print("OK")
    return NavigateResponse()


s = rospy.Service('navigate', Navigate, handle_navigate)
m1 = rospy.Publisher("/motor1", Float32, queue_size=10)
m2 = rospy.Publisher("/motor2", Float32, queue_size=10)

r = rospy.Rate(config["update_rate"])  # 10hz
yaw_pid = PID(config["yaw_pid"]["p"], config["yaw_pid"]
              ["i"], config["yaw_pid"]["d"])
while not rospy.is_shutdown():
    # global nav_state
    # calc()
    # print(nav_state, mode)
    if nav_state == "start":
        print(nav_state, mode)
        yaw_to_point = math.atan2(target_y-r_y, target_x-r_x)
        start_yaw = r_yaw
        nav_state = "rotate"
        yaw_pid = PID(
            config["yaw_pid"]["p"], config["yaw_pid"]["i"], config["yaw_pid"]["d"])
        # yaw_pid = PID(config["yaw_pid"]["p"], config["yaw_pid"]["i"], config["yaw_pid"]["d"])
    if nav_state == "rotate":
        print(nav_state, mode)
        print("yaw_to_point", yaw_to_point)
        if (abs(offset_yaw(r_yaw, yaw_to_point)) >= config["yaw_th"]):
            v = motors_config["robot_W"] * config["yaw_speed"]
            mv1 = v * ((offset_yaw(r_yaw, yaw_to_point) > 0)*2-1)
            mv2 = -v * ((offset_yaw(r_yaw, yaw_to_point) > 0)*2-1)
            m1.publish(float(mv1))
            m2.publish(float(mv2))
            print("Yaw", r_yaw)
        if (abs(offset_yaw(r_yaw, yaw_to_point)) < config["yaw_th"]):
            print("OK")
            if mode != "yaw":
                nav_state = "going"
                m1.publish(float(0))
                m2.publish(float(0))
                yaw_pid = PID(
                    config["yaw_pid"]["p"], config["yaw_pid"]["i"], config["yaw_pid"]["d"])
            else:
                if target_stopper == True:
                    m1.publish(float(0))
                    m2.publish(float(0))
                nav_state = "done"
    if nav_state == "going":
        yaw_to_point = math.atan2(target_y-r_y, target_x-r_x)
        pid_r = yaw_pid.calc(offset_yaw(r_yaw, yaw_to_point))
        m1.publish(float(target_speed + pid_r))
        m2.publish(float(target_speed - pid_r))
        print("sp left", float(target_speed - pid_r), float(target_speed + pid_r))
        # print(get_dist(r_x, r_y, target_x, target_y), float(config["dist_th"]))
        if get_dist(r_x, r_y, target_x, target_y) < float(config["dist_th"]):
            # global nav_state
            print("TRUE", nav_state)
            nav_state = "done"
            print("TRUE2", nav_state)
            print(nav_state)
            if target_stopper == True:
                m1.publish(float(0))
                m2.publish(float(0))

    # if nav_state == "done":
    #     nav_state = "wait"
    # m1.publish(float(0))
    # m2.publish(float(0))

    r.sleep()
