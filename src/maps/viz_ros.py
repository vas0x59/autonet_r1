#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import cv2
import random
from graph import Graph

import rospy
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
import tf


rospy.init_node('viz', anonymous=True)
map_path = rospy.get_param("~map", "map_1.json")
map_c_path = rospy.get_param("~map_coordinates", "map_coordinates_1.json")
pole_img_path = rospy.get_param("~pole_img", "pole.jpg")
print(map_path, map_c_path, pole_img_path)

d = json.load(open(map_path))

coordinates = json.load(open(map_c_path))
g = Graph(d)
random.seed(22)


pole = cv2.imread(pole_img_path)
pole = cv2.resize(pole, (0, 0), fx=0.15, fy=0.15)


r_x = 0
r_y = 0
r_yaw = 0
def nav_clb(data: Pose):
    global r_x, r_y, r_yaw
    r_x = data.position.x
    r_y = data.position.y
    r_yaw = tf.transformations.euler_from_quaternion(
        data.pose.pose.orientation.w, data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z)[2]


nav_sub = rospy.Subscriber("/nav", Pose, nav_clb)

font = cv2.FONT_HERSHEY_SIMPLEX
# bottomLeftCornerOfText = (10,500)
fontScale = 0.5
fontColor = (0, 0, 255)
lineType = 2


for type, coord in coordinates.items():
    x = coord[0]
    y = coord[1]
    plt.scatter(x, y)
    plt.text(x - 0.1, y + 0.1, type, fontsize=7, )
    ix = (x)*pole.shape[1]/8
    iy = pole.shape[0] - (y)*pole.shape[1]/8
    pole = cv2.circle(pole, (int(ix), int(iy)), 5, (0, 255, 0), thickness=-1)
    cv2.putText(pole, type,
                (int(ix), int(iy-5-random.random()*15)),
                font,
                fontScale,
                fontColor,
                lineType)
    l = list(d[type])
    for i in l:
        iix = (coordinates[i[0]][0])*pole.shape[1]/8
        iiy = pole.shape[0] - (coordinates[i[0]][1])*pole.shape[1]/8
        if "cross" in type and "cross" in i[0] or "round" in type and "round" in i[0]:
            cv2.arrowedLine(pole, (int(ix), int(iy)), (int(
                iix), int(iiy)), (0, 255, 150), thickness=2)
        else:
            cv2.arrowedLine(pole, (int(ix), int(iy)), (int(
                iix), int(iiy)), (0, 150, 255), thickness=2)

while cv2.waitKey(1) != ord("q"):
    pole_d = pole.copy()

    ix = (r_x)*pole.shape[1]/8
    iy = pole.shape[0] - (r_y)*pole.shape[1]/8
    cv2.circle(pole, (int(ix), int(iy)), 5, (255, 0, 255), thickness=-1)
    cv2.imshow("pole", pole_d)
# def viz_path(path, pole_d):
#     for j in range(len(path) - 1):
#         x = coordinates[path[j]][0]
#         y = coordinates[path[j]][1]
#         ix = (x)*pole.shape[1]/8
#         iy = pole.shape[0] - (y)*pole.shape[1]/8
#         # i = d[path[j+1]]
#         iix = (coordinates[path[j+1]][0])*pole.shape[1]/8
#         iiy = pole.shape[0] - (coordinates[path[j+1]][1])*pole.shape[1]/8
#         cv2.arrowedLine(pole_d, (int(ix), int(iy)), (int(iix),
#                                                    int(iiy)), (255, 0, 0), thickness=2)


# # plt.show()
# # plt.savefig('graph.png')
# cv2.imshow("pole", pole)

# # cv2.waitKey(0)
# while cv2.waitKey(1) != ord("q"):
#     pole_d = pole.copy()
#     p1 = input("p1: ")
#     p2 = input("p2: ")
#     if p1 == "q":
#         break
#     path, d = g.find_path(p1, p2)
#     viz_path(path, pole_d)
#     print(path)
#     cv2.imshow("pole", pole_d)
