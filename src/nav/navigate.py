#!/usr/bin/env python3


import rospy
import tf
import math
import numpy as np
import json

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped

from autonet_r1.srv import Navigate, NavigateResponse
from autonet_r1.src.motors import PID

"""
"""

rospy.init_node('navigate')
config_path = rospy.get_param("~config", "navigate_config.json")
config = json.load(open(config_path))
print(config)

mode = "disable"
target_stopper = True
target_x = 0
target_y = 0
target_yaw = 0
target_speed = 0
time_r = 0
# rospy.Time.now().to_sec()
x = 0
y = 0
yaw = 0


def nav_clb(data: Pose):
    global x, y, yaw
    x = data.position.x
    y = data.position.y
    yaw = tf.transformations.euler_from_quaternion(
        data.pose.pose.orientation.w, data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z)[2]


nav_sub = rospy.Subscriber("/nav", Pose, nav_clb)


def handle_navigate(req: Navigate):
    global mode, target_x, target_y, target_yaw, target_speed, time_r, target_stopper
    time_r = rospy.Time.now().to_sec()
    target_x = req.x
    target_y = req.y
    target_yaw = req.yaw
    mode = req.mode
    target_stopper = req.stopper
    target_speed = req.speed

    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    return NavigateResponse(0)



s = rospy.Service('navigate', Navigate, handle_navigate)


r = rospy.Rate(config["update_rate"])  # 10hz
while not rospy.is_shutdown():
    # calc()
    r.sleep()