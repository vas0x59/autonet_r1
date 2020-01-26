#!/usr/bin/env python3


import rospy
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped

from autonet_r1.srv import Navigate, NavigateResponse
from autonet_r1.src.motors import PID

"""
"""

mode = "enable"
target_x = 0
target_y = 0
target_yaw = 0
target_speed = 0

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


def handle_navigate(req):
    global mode, target_x, target_y, target_yaw, target_speed

    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    return NavigateResponse(0)


rospy.init_node('add_two_ints_server')
s = rospy.Service('navigate', Navigate, handle_navigate)
