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
from autonet_r1.src.motors.PID import PID

p1 = "s1"
p2 = input("p2")

# recog = rec()
# reg = False
# while True:
#     t, c = recog.recog()
#     if len(t) > 0:
#         break

# recog.recog()


rospy.init_node("do_way", anonymous=True)

# Config
map_path = rospy.get_param("~map", "../maps/map_1.json")
map_c_path = rospy.get_param(
    "~map_coordinates", "../maps/map_coordinates_1.json")
print(map_path, map_c_path)

map_conn = json.load(open(map_path))
map_coor = json.load(open(map_c_path))

config_path = rospy.get_param("~config", "./line_params.json")
config = json.load(open(config_path))
print(config_path, config)
E1_K = config["E1_K"]
E2_K = config["E2_K"]
PID_P = config["pid"]["p"]
PID_I = config["pid"]["i"]
PID_D = config["pid"]["d"]


# Movements Services
get_telemetry = rospy.ServiceProxy('get_telemetry', GetTelemetry)
navigate = rospy.ServiceProxy('navigate', Navigate)
set_nav = rospy.ServiceProxy('set_nav', SetNav)
get_path = rospy.ServiceProxy('get_path', GetPath)
get_grab_path = rospy.ServiceProxy('get_grab_path', GetGrabPath)
path_pub = rospy.Publisher('/path', PathNamed3)


def navigate_wait(x=0, y=0, yaw=0, speed=0.2, frame="nav", stopper=True, mode='', th=0.03, id=""):
    navigate(x=x, y=y, yaw=yaw, speed=speed, frame=frame, stopper=stopper,
             id="navigate_wait_"+str(round(rospy.Time.now().to_sec(), 1)), mode=mode)
    r = rospy.Rate(10)  # 10hz
    while True:
        telem = get_telemetry(frame=frame)
        # print(telem)
        if get_dist(x, y, telem.x, telem.y) < th:
            break
        r.sleep()

# Line


def lr_clb(data):
    global lr_e1, lr_e2, lr_color
    lr_e1 = data.e1
    lr_e2 = data.e2
    lr_color = data.color


lane_res = rospy.Subscriber("/lane/res", LaneRes, lr_clb)
# m1 = rospy.Publisher("/motor1", Float32, queue_size=10)
# m2 = rospy.Publisher("/motor2", Float32, queue_size=10)
cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

pid_l = PID(PID_P, PID_I, PID_D)


def calc_line():
    global m1, m2, lr_e1, lr_e2, lr_color, pid_l, E1_K, E2_K, target_speed
    error = (lr_e1*E1_K + lr_e2*E2_K)
    print("err", error, "e1", lr_e1, "e2", lr_e2)

    a = -pid_l.calc(error - 0)
    # m1.publish(float(target_speed - a))
    # m2.publish(float(target_speed + a))
    tw = Twist()
    tw.linear.x = target_speed
    tw.angular.z = a
    cmd_vel.publish(tw)


# Path
path = get_path(start=p1, end=p2).path
print(path)
path_pub.publish(PathNamed3(path=path, start=p1, end=p2))


def get_typeof_point(s: str):
    if "cross" in s:
        return "cross", s.split("_")[0][len("cross"):], s.split("_")[1]
    elif "corner" in s:
        return "corner", s.split('_')[0][len("corner"):], s.split('_')[1], s.split('_')[2]
    elif "grab" in s:
        return "grab", s[len("grab"):]
    else:
        return "building", s[0], s[1:]


def get_typeof_transition(p1, p2):
    if p1[0] == "building" and p2[0] == "building":
        return "lane_follow"
    elif p1[0] == "corner" and p2[0] == "corner":
        return "corner"
    elif (p1[0] == "building" or p1[0] == "grab") and p2[0] == "corner":
        return "lane_follow"
    elif p1[0] == "corner" and (p2[0] == "building" or p2[0] == "grab"):
        return "lane_follow"
    elif (p1[0] == "building" or p1[0] == "grab") and p2[0] == "cross":
        return "lane_follow_cor"
    elif p1[0] == "cross" and (p2[0] == "building" or p2[0] == "grab"):
        return "lane_follow"
    else:
        return "navigate"


set_nav(x=0, y=0, yaw=0, mode="")
rospy.sleep(1)

print("Path", path[0:])
prev_point = p1

for point_name in ["round1_1", "g1"]:
    x, y = tuple(map_coor[point_name])
    # print(x, y)
    x, y = map_to_odom(x, y, map_coor[p1][0], map_coor[p1][1], p1)
    print(x, y)
    # break
    navigate_wait(x=x, y=y, yaw=0, speed=0.3,
                  frame="nav", stopper=True, mode='')
    prev_point = point_name
    rospy.sleep(0.15)



for point_name in path[3:]:
    trans_type = get_typeof_transition(prev_point, point_name)
    x, y = tuple(map_coor[point_name])
    # print(x, y)
    x, y = map_to_odom(x, y, map_coor[p1][0], map_coor[p1][1], p1)
    print(x, y)
    # break
    navigate_wait(x=x, y=y, yaw=0, speed=0.3,
                  frame="nav", stopper=True, mode='')
    prev_point = point_name
    rospy.sleep(0.15)
