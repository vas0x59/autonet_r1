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
from autonet_r1.msg import LaneRes, Addres, PathNamed3, PathNamed2
from autonet_r1.src.tools.tf_tools import *


p1 = input("start")
p2 = input("p2")

rospy.init_node("get_path")
map_path = rospy.get_param("~map", "../maps/map_1.json")
map_c_path = rospy.get_param(
    "~map_coordinates", "../maps/map_coordinates_1.json")
print(map_path, map_c_path)

map_conn = json.load(open(map_path))
map_coor = json.load(open(map_c_path))

get_telemetry = rospy.ServiceProxy('get_telemetry', GetTelemetry)
navigate = rospy.ServiceProxy('navigate', Navigate)
set_nav = rospy.ServiceProxy('set_nav', SetNav)
get_path = rospy.ServiceProxy('get_path', GetPath)
get_grab_path = rospy.ServiceProxy('get_grab_path', GetGrabPath)
path_pub = rospy.Publisher('/path', PathNamed3)

path = get_path(start=p1, end=p2).path
print(path)
path_pub.publish(PathNamed3(path=path, start=p1, end=p2))

# def navigate_wait(x=0, y=0, yaw=0, frame=0, th=0.02):
#     # while
#     pass
for point_name in path:
    x, y = tuple(map_coor[point_name])
    navigate(x=x, y=y, yaw=float('nan'), speed=0.4, frame="map", stopper=False, id="get_path_nav_"+str(round(rospy.Time.now().to_sec(), 1)))
    while True:
        telem = get_telemetry()
        if get_dist(x, y, telem.x, telem.y) < 0.05:
            break
