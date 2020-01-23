import rospy
from std_msgs.msg import Int16


m1 = rospy.Publisher('chatter', String, queue_size=10)


