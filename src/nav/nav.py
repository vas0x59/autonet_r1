#!/usr/bin/env python3
import rospy
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
from autonet_r1.srv import SetOdom, SetNav
import math
import json

"""
Modes:  1 - ALL
        2 - Zero
"""

rospy.init_node('nav', anonymous=True)
config_path = rospy.get_param("~config", "nav_config.json")
config = json.load(open(config_path))
print(config)


odom_x = 0
odom_y = 0
odom_yaw = 0

navx_yaw = 0

res_x = 0
res_y = 0
res_yaw = 0

zero_x = 0
zero_y = 0
zero_yaw = 0

nav_pub = rospy.Publisher('nav', Pose, queue_size=50)
nav_broadcaster = tf.TransformBroadcaster()


def odom_clb(data: Odometry):
    global odom_x, odom_y, odom_yaw
    odom_x = data.pose.pose.position.x
    odom_y = data.pose.pose.position.y
    odom_yaw = tf.transformations.euler_from_quaternion(
        data.pose.pose.orientation.w, )[2]


odom_sub = rospy.Subscriber("/odom", Odometry, odom_clb)
set_odom = rospy.ServiceProxy('set_odom', SetOdom)


def set_nav(data):
    global zero_x, zero_y, zero_yaw, res_x, res_y, res_yaw
    if data.mode == 1:
        set_odom(x=data.x, y=data.y, yaw=data.yaw)
        res_x = data.x
        res_y = data.y
        rex_yaw = data.yaw
    else:
        zero_x = data.x
        zero_y = data.y
        zero_yaw = data.yaw


s = rospy.Service('set_nav', SetNav, set_nav)


def calc():
    global odom_x, odom_y, odom_yaw, navx_yaw, zero_x, zero_y, zero_yaw, res_x, res_y, res_yaw
    res_x = (odom_x*config["odom_xy_w"]) / (config["odom_xy_w"]) - zero_x
    res_y = (odom_y*config["odom_xy_w"]) / (config["odom_xy_w"]) - zero_y
    res_yaw = (odom_yaw*config["odom_yaw_w"] + navx_yaw*config["navx_yaw_w"]
               ) / (config["odom_yaw_w"] + config["odom_navx_w"]) - zero_yaw
    
    current_time = rospy.Time.now()
    quat = tf.transformations.quaternion_from_euler(0, 0, res_yaw)
    nav_broadcaster.sendTransform(
        (res_x, res_y, 0.),
        quat,
        current_time,
        "base_link",
        "nav"
    )
    pose = PoseStamped()
    pose.header.stamp = current_time
    pose.header.frame_id = "nav"
    
    # set the position
    pose.pose = Pose(Point(res_x, res_y, 0.), Quaternion(*quat))
    nav_pub.publish(pose)
    
    # set the velocity
    # pose.child_frame_id = "base_link"


r = rospy.Rate(config["update_rate"])  # 10hz
while not rospy.is_shutdown():
    calc()
    r.sleep()
