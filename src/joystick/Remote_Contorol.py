#!/usr/bin/env python3
import rospy
import inputs
from std_msgs.msg import Float32
from std_msgs.msg import Int16
import time
import json

pads = inputs.devices.gamepads
print(pads)
if len(pads) == 0:
    raise Exception("Couldn't find any Gamepads!")


def main():
    lj = "ABS_Y"
    rj = "ABS_RY"
    a = "BTN_SOUTH"
    b = "BTN_EAST"
    x = "BTN_NORTH"
    y = "BTN_WEST"
    # events = inputs.get_gamepad()
    pub1 = rospy.Publisher("/motor1", Float32, queue_size=10)
    pub2 = rospy.Publisher("/motor2", Float32, queue_size=10)
    pub3 = rospy.Publisher("/arduino/servo1", Int16,
                           queue_size=10)  # servo grab
    pub4 = rospy.Publisher("/arduino/servo2", Int16,
                           queue_size=10)  # servo up/down
    # rospy.spin()
    rospy.init_node("joystick", anonymous=True)
    config_path = rospy.get_param("~config", "config.json")
    config = json.load(open(config_path))
    # r = rospy.Rate(10)
    while not rospy.is_shutdown():
        events = inputs.get_gamepad()
        for event in events:
            # print(event)
            if (event.code == lj) and ((-32000 < event.state < -0.05/32000) or (0.05/32000 < event.state < 32000)):
                ur1 = event.state/-32000 * config["speed"]
                # print(ur1)
                pub1.publish(ur1)
            if (event.code == rj) and ((-32000 < event.state < -0.05/32000) or (0.05/32000 < event.state < 32000)):
                ur2 = event.state / -32000 * config["speed"]
                pub2.publish(ur2)
            if (event.code == a) and (event.state == 1):
                pub3.publish(60)
            if (event.code == b) and (event.state == 1):
                pub3.publish(180)
            # if (event.code == y) and (event.state == 1):
            #     pub4.publish(180)
            # elif (event.code == x) and (event.state == 1):
            #     pub4.publish(0)
            # else:
            #     pub4.publish(90)
            if (event.code == x):
                exit()
            # r.sleep()
            # rospy.sleep(0.01)


try:
    main()
except rospy.ROSInterruptException:
    pass
