#!/usr/bin/env python3
import rospy
import tf
# import tf2_ros
# import tf2_geometry_msgs
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped, TransformStamped
from autonet_r1.srv import SetOdom, SetNav, SetNavResponse, GetTelemetry, GetTelemetryResponse
import math
import json
from autonet_r1.src.tools.tf_tools import *

"""
Modes:  1 - ALL
        2 - Zero
"""

rospy.init_node('nav')
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

nav_pub = rospy.Publisher('nav', PoseStamped, queue_size=50)
nav_broadcaster = tf.TransformBroadcaster()
# tf_buffer = tf2_ros.Buffer()
# tf_listener = tf2_ros.TransformListener(tf_buffer)
listener = tf.TransformListener()
# tf_buffer.transform()

# listener.
# listener.
def odom_clb(data: Odometry):
    global odom_x, odom_y, odom_yaw
    odom_x = data.pose.pose.position.x
    odom_y = data.pose.pose.position.y
    odom_yaw = tf.transformations.euler_from_quaternion([
        data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w])[2]


odom_sub = rospy.Subscriber("/odom", Odometry, odom_clb)
set_odom = rospy.ServiceProxy('set_odom', SetOdom)


def set_nav(data):
    global zero_x, zero_y, zero_yaw, res_x, res_y, res_yaw
    if data.mode == "all":
        set_odom(x=data.x, y=data.y, yaw=data.yaw)
        res_x = data.x
        res_y = data.y
        rex_yaw = data.yaw
    else:
        zero_x = data.x
        zero_y = data.y
        zero_yaw = data.yaw
    return SetNavResponse()


def get_tem(data):
    global res_x, res_y, res_yaw, listener
    # res = GetTelemetryResponse()
    # tf_buffer.t
    # res.x =
    x, y, yaw = transform_xy_yaw(
        res_x, res_y, res_yaw, "nav", data.frame, listener)
    # res.x = x
    # res.y = y
    # res.yaw = yaw
    return {"x": x, "y": y, "yaw": yaw}


s = rospy.Service('set_nav', SetNav, set_nav)
gs = rospy.Service('get_telemetry', GetTelemetry, get_tem)


def calc():
    global odom_x, odom_y, odom_yaw, navx_yaw, zero_x, zero_y, zero_yaw, res_x, res_y, res_yaw
    res_x = (odom_x*config["odom_xy_w"]) / (config["odom_xy_w"]) - zero_x
    res_y = (odom_y*config["odom_xy_w"]) / (config["odom_xy_w"]) - zero_y
    res_yaw = offset_yaw((odom_yaw*config["odom_yaw_w"] + navx_yaw*config["navx_yaw_w"]
               ) / (config["odom_yaw_w"] + config["navx_yaw_w"]), zero_yaw)

    current_time = rospy.Time.now()
    quat = tf.transformations.quaternion_from_euler(0, 0, res_yaw)
    nav_broadcaster.sendTransform(
        (res_x, res_y, 0.),
        quat,
        current_time,
        "base_link",
        "nav")

    # nav_broadcaster.sendTransform(
    #     (0, 0, 0.),
    #     (0, 0, 0, 0),
    #     current_time,
    #     "odom",
    #     "nav"
    # )
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
