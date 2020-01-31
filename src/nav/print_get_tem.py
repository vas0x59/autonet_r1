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

rospy.init_node("TESt_TEM", anonymous=True)
get_telemetry = rospy.ServiceProxy('get_telemetry', GetTelemetry)
r = rospy.Rate(2)
while True:
    # print("nav", get_telemetry(frame="nav"))
    print(get_telemetry(frame="map"))
    r.sleep()