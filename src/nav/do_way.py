#!/usr/bin/env python3
# import sys
# # sys.path.append('../../../autonet_r1')
# print(sys.path)
import rospy
import tf
import math
import numpy as np
import json

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
from std_msgs.msg import Float32

from autonet_r1.srv import Navigate