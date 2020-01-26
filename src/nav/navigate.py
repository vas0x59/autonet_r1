#!/usr/bin/env python3

from autonet_r1.srv import Navigate, NavigateResponse
import rospy

def handle_navigate(req):
    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    return NavigateResponse(0)

def navigate_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('navigate', AddTwoInts, handle_add_two_ints)
    # print "Ready to add two ints."
    # rospy.spin()


if __name__ == "__main__":
    navigate_server()