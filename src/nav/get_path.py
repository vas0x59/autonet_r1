from autonet_r1.src.maps.graph import Graph
import json 

import rospy
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseStamped
import tf2_ros
import tf

from autonet_r1.srv import GetPath, GetPathResponse

map_path = rospy.get_param("~map", "../maps/map_1.json")
map_c_path = rospy.get_param("~map_coordinates", "../maps/map_coordinates_1.json")
print(map_path, map_c_path)

d = json.load(open(map_path))
coordinates = json.load(open(map_c_path))
g = Graph(d)

def handle_get_path(req):
    path = []
    if req.stop == "":
        path, d = g.find_path(req.start, req.end)
    return GetPathResponse(path)

s = rospy.Service('get_path', GetPath, handle_get_path)
rospy.spin()