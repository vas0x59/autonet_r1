#!/usr/bin/env python3

import rospy
import tf
import math
import numpy as np
import json

from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
from std_msgs.msg import Float32, Header

from autonet_r1.srv import Navigate, GetPath, SetNav, GetTelemetry, GetGrabPath
from autonet_r1.msg import LaneRes, PathNamed3, PathNamed2
from autonet_r1.src.tools.tf_tools import *
import autonet_r1.src.tools.calc_trajectory as calc_trajectory
from autonet_r1.src.nav.coor_conv import *
from autonet_r1.src.digitRecognition.rec import *
from autonet_r1.src.motors.PID import PID

start_point = "s1"
point_to = input("p2")

# recog = rec()
# reg = False
# while True:
#     t, c = recog.recog()
#     if len(t) > 0:
#         break

# recog.recog()


rospy.init_node("do_way", anonymous=True)

# Config
map_path = rospy.get_param("~map", "../src/maps/map_1.json")
map_c_path = rospy.get_param(
    "~map_coordinates", "../src/maps/map_coordinates_1.json")
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
path_nav_pub = rospy.Publisher('/path_ros', Path)



def navigate_wait(x=0, y=0, yaw=0, speed=0.2, frame="nav", stopper=True, mode='', th=0.06, id=""):
    navigate(x=x, y=y, yaw=yaw, speed=speed, frame=frame, stopper=stopper,
             id="navigate_wait_"+str(round(rospy.Time.now().to_sec(), 1)), mode=mode, th=th)
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
    global m1, m2, lr_e1, lr_e2, lr_color, pid_l, E1_K, E2_K, target_speed, cmd_vel
    error = (lr_e1*E1_K + lr_e2*E2_K)
    print("err", error, "e1", lr_e1, "e2", lr_e2)

    a = -pid_l.calc(error - 0)
    # m1.publish(float(target_speed - a))
    # m2.publish(float(target_speed + a))
    tw = Twist()
    tw.linear.x = 0.21
    tw.angular.z = a
    cmd_vel.publish(tw)


# Path
path = get_path(start=start_point, end=point_to).path
print(path)
path_pub.publish(PathNamed3(path=path, start=start_point, end=point_to))
path_nav = Path()
path_nav.header.frame_id = "nav"
path_nav.poses = [PoseStamped(header=Header(frame_id="nav"), pose=Pose(position=Point(x, y, 0))) for x, y in [map_to_odom(
    map_coor[p][0], map_coor[p][1], map_coor[start_point][0], map_coor[start_point][1], start_point) for p in path]]
path_nav_pub.publish(path_nav)
# PoseStamped().pose.position.


def get_typeof_point(s: str):
    if "cross" in s:
        return "cross", s.split("_")[0][len("cross"):], s.split("_")[1]
    elif "corner" in s:
        return "corner", s.split('_')[0][len("corner"):], s.split('_')[1], s.split('_')[2]
    elif "grab" in s:
        return "grab", s[len("grab"):]
    elif "round" in s:
        return "cross", s.split("_")[0][len("cross"):], s.split("_")[1]
    else:
        return "building", s[0], s[1:]


def get_typeof_transition(p1, p2):
    if p1[0] == "building" and p2[0] == "building":
        return "lane_follow"
    elif p1[0] == "corner" and p2[0] == "corner":
        if p1[2] == "s":
            return "lane_follow"
        else:
            return "corner"
    elif (p1[0] == "building" or p1[0] == "grab") and p2[0] == "corner":
        return "lane_follow"
    elif p1[0] == "corner" and (p2[0] == "building" or p2[0] == "grab"):
        return "lane_follow"
        # return "navigate"
    elif (p1[0] == "building" or p1[0] == "grab") and p2[0] == "cross":
        return "lane_follow_cor"
    elif p1[0] == "cross" and (p2[0] == "building" or p2[0] == "grab"):
        return "lane_follow"
        # return "navigate"
    elif p1[0] == "cross" and p2[0] == "cross":
        return "cross"
    else:
        return "navigate"


def lane_follow_transition(p1, p2):
    global calc
    th = 0.1
    if get_typeof_point(p1)[0] == "corner":
        if get_typeof_point(p1)[2] == "s":
            th = 0.4
    if get_typeof_point(p2)[0] == "corner":
        if get_typeof_point(p2)[2] == "s":
            th = 0.4
    x_m, y_m = tuple(map_coor[p2])
    # print(x, y)
    x, y = map_to_odom(
        x_m, y_m, map_coor[start_point][0], map_coor[start_point][1], start_point)
    navigate(x=x, y=y, yaw=0, speed=0.25,
             frame="nav", stopper=True, mode='yaw', id="yaw_cor")
    if get_typeof_point(p1)[0] == "building" and get_typeof_point(p2)[0] == "building":
        rospy.sleep(1)
    else:
        rospy.sleep(4)
    r = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        calc_line()
        r.sleep()
        telem = get_telemetry(frame="nav")
        if get_dist(x, y, telem.x, telem.y) < th:
            break
    tw = Twist()
    tw.linear.x = 0
    tw.angular.z = 0
    cmd_vel.publish(tw)
    return "DONE"


def navigate_transition(p1, p2):
    x_m, y_m = tuple(map_coor[p2])
    # print(x, y)
    x, y = map_to_odom(
        x_m, y_m, map_coor[start_point][0], map_coor[start_point][1], start_point)
    print("INFO", "COOR_TO", x, y)
    # break
    navigate_wait(x=x, y=y, yaw=0, speed=0.25,
                  frame="nav", stopper=True, mode='')
    return "DONE"


def cross_transition(p1, p2):
    x_m, y_m = tuple(map_coor[p2])
    # print(x, y)
    x, y = map_to_odom(
        x_m, y_m, map_coor[start_point][0], map_coor[start_point][1], start_point)
    print("INFO", "COOR_TO", x, y)
    # break
    navigate_wait(x=x, y=y, yaw=0, speed=0.25,
                  frame="nav", stopper=True, mode='')
    return "DONE"


def corner_transition(p1, p2):
    x_m, y_m = tuple(map_coor[p2])
    # print(x, y)
    x, y = map_to_odom(
        x_m, y_m, map_coor[start_point][0], map_coor[start_point][1], start_point)
    telem = get_telemetry(frame="nav")
    tr = calc_trajectory.find_trajectory([telem.x, telem.y],[x, y], telem.yaw)
    print("INFO", "COOR_TO", x, y)
    # break
    for p in tr:
        navigate_wait(x=p[0], y=p[1], yaw=0, speed=0.1,
                    frame="nav", stopper=False, mode='only_atan', th=0.1)
    navigate_wait(x=p[0], y=p[1], yaw=0, speed=0.25,
                    frame="nav", stopper=True, mode='')
    return "DONE"


transition_funs = {"lane_follow": lane_follow_transition,
                   "cross": cross_transition, "navigate": navigate_transition,
                   "corner": corner_transition, "lane_follow_cor": lane_follow_transition}

set_nav(x=0, y=0, yaw=0, mode="")
rospy.sleep(1)

print("Path", path[0:])
prev_point = start_point

for point_name in ["round1_1", "g1"]:
    path_nav_pub.publish(path_nav)
    x, y = tuple(map_coor[point_name])
    # print(x, y)
    x, y = map_to_odom(
        x, y, map_coor[start_point][0], map_coor[start_point][1], start_point)
    print(x, y)
    # break
    navigate_wait(x=x, y=y, yaw=0, speed=0.25,
                  frame="nav", stopper=True, mode='')
    prev_point = point_name
    rospy.sleep(0.15)


for point_name in path[3:]:
    path_nav_pub.publish(path_nav)
    trans_type = get_typeof_transition(get_typeof_point(
        prev_point), get_typeof_point(point_name))
    print("INFO", trans_type, "FROM", prev_point, "TO", point_name)
    if trans_type in transition_funs.keys():
        transition_funs[trans_type](prev_point, point_name)
    else:
        print("WARN", "transition not found", "GO BY NAVIGATE")
        x_m, y_m = tuple(map_coor[point_name])
        # print(x, y)
        x, y = map_to_odom(
            x_m, y_m, map_coor[start_point][0], map_coor[start_point][1], start_point)
        print("INFO", "COOR_TO", x, y)
        # break
        navigate_wait(x=x, y=y, yaw=0, speed=0.25,
                      frame="nav", stopper=True, mode='')
    prev_point = point_name
    print("INFO", "TO", point_name, "DONE")
    rospy.sleep(0.15)
navigate_wait(x=0, y=0, yaw=0, speed=0.4,
              frame="nav", stopper=True, mode='')
