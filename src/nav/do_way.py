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
from autonet_r1.src.nav.coor_conv import *
from autonet_r1.src.digitRecognition.rec import *

p1 = "s1"
p2 = input("p2")

recog = rec()
# reg = False
while True:
    t, c = recog.recog()
    if len(t) > 0:
        break

# recog.recog()



rospy.init_node("do_way", anonymous=True)
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

# def convert(x, y, ps):
#     xr = 0
#     yr = 0
#     if ps == "s1":
#         xr = -(y - map_coor["s1"][1])
#         yr = -(-x - map_coor["s1"][0])
#     elif ps == "s2":
#         xr = -y - map_coor["s2"][0]
#         yr = x - map_coor["s2"][1]
#     return xr, yr
# set_nav(x=0, y=0, yaw=0, mode="all")
set_nav(x=0, y=0, yaw=0, mode="all")
rospy.sleep(1)
# def navigate_wait(x=0, y=0, yaw=0, frame=0, th=0.02):
#     # while
#     pass

# x, y = convert(map_coor["round1_1"][0], map_coor["round1_1"][1], p1)    
# print(x, y)
navigate(x=0.4, y=0, yaw=0, speed=0.4, frame="nav", stopper=True, id="123", mode='')
while True:
    telem = get_telemetry(frame="nav")
    if get_dist(0.4, 0, telem.x, telem.y) < 0.05:
        break
navigate(x=0.4, y=0.42, yaw=0, speed=0.4, frame="nav", stopper=True, id="123", mode='')
while True:
    telem = get_telemetry(frame="nav")
    if get_dist(0.4, 0.42, telem.x, telem.y) < 0.05:
        break
navigate(x=1.1, y=0.42, yaw=0, speed=0.4, frame="nav", stopper=True, id="123", mode='')
while True:
    telem = get_telemetry(frame="nav")
    if get_dist(1.1, 0.42, telem.x, telem.y) < 0.05:
        break

# while True:
#     telem = get_telemetry(frame="nav")
#     if get_dist(x, y, telem.x, telem.y) < 0.05:
#         break
print("PATH", path[3:])

for point_name in path[3:]:
    x, y = tuple(map_coor[point_name])
    # print(x, y)
    x, y = map_to_odom(x-0.1, y, map_coor[p1][0], map_coor[p1][1], p1)
    print(x, y)
    # break
    navigate(x=x, y=y, yaw=0, speed=0.4, frame="nav", stopper=True, id="get_path_nav_"+str(round(rospy.Time.now().to_sec(), 1)), mode='')
    while True:
        telem = get_telemetry(frame="nav")
        # print(telem)
        if get_dist(x, y, telem.x, telem.y) < 0.05:
            break
    rospy.sleep(5)
