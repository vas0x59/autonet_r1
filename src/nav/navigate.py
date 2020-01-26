#!/usr/bin/env python3

from autonet_r1.srv import Navigate, NavigateResponse
import rospy


"""
"""

state = "enable"
target_x = 0
target_y = 0
target_yaw = 0

def handle_navigate(req):
    global state

    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    return NavigateResponse(0)

def navigate_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('navigate', Navigate, handle_navigate)
    # print "Ready to add two ints."
    # rospy.spin()


if __name__ == "__main__":
    navigate_server()