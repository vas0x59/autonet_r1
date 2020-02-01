#!/usr/bin/env python3
import rospy
import inputs
import rosbag
from std_msgs.msg import Float32, Int16
import time
import json

pads = inputs.devices.gamepads
bag = rosbag.Bag('win.bag', 'w')
bag1 = rosbag.Bag('win.bag')
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
    q = "BTN_START"
    z = "ABS_HAT0X"
    c = "ABS_HAT0Y"
    i1 = Float32()
    i2 = Float32()
    i3 = Int16()
    i4 = Int16()
    pub1 = rospy.Publisher("/motor1", Float32, queue_size=10)
    pub2 = rospy.Publisher("/motor2", Float32, queue_size=10)
    pub3 = rospy.Publisher("/arduino/servo1", Int16,
                           queue_size=10)  # servo up/down
    pub4 = rospy.Publisher("/arduino/servo2", Int16,
                           queue_size=10)  # servo grab
    rospy.init_node("joystick", anonymous=True)
    config_path = rospy.get_param("~config", "config.json")
    config = json.load(open(config_path))
    while not rospy.is_shutdown():
        events = inputs.get_gamepad()
        for event in events:
            if (event.code == lj) and ((-32000 < event.state < -0.05/32000) or (0.05/32000 < event.state < 32000)):
                ur1 = event.state/-32000 * config["speed"]
                pub1.publish(ur1)
                i1.data = ur1
                bag.write('/motor1', i1)
            if (event.code == rj) and ((-32000 < event.state < -0.05/32000) or (0.05/32000 < event.state < 32000)):
                ur2 = event.state / -32000 * config["speed"]
                pub2.publish(ur2)
                i2.data = ur2
                bag.write('/motor2', i2)
            if (event.code == a) and (event.state == 1):
                pub3.publish(180)
                i3.data = 180
                bag.write('/arduino/servo1', i3)
            if (event.code == b) and (event.state == 1):
                pub4.publish(180)
                i4.data = 180
                bag.write('/arduino/servo2', i4)
            if (event.code == y) and (event.state == 1):
                pub3.publish(0)
                i3.data = 0
                bag.write('/arduino/servo1', i3)
            if (event.code == x) and (event.state == 1):
                pub4.publish(0)
                i4.data = 0
                bag.write('/arduino/servo2', i4)
            if (event.code == c) and (event.state == 1):
                bag.close()
            if (event.code == z) and (event.state == 1):
                for topic, msg, t in bag.read_messages(topics=['/motor1', '/motor2','/arduino/servo1','/arduino/servo2']):
                    pub1.publish(msg[0])
                    pub2.publish(msg[1])
                    pub3.publish(msg[2])
                    pub4.publish(msg[3])
                    rate.sleep()
                bag.close
            if (event.code == q):
                exit()


try:
    main()
except rospy.ROSInterruptException:
    pass