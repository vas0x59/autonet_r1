import rospy
import tf
import tf2_ros


from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int16, Bool
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped

def get_transform(msg):
    # br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()

    t.header.stamp = msg[2]
    t.header.frame_id = msg[4]
    t.child_frame_id = msg[3]
    t.transform.translation.x = msg[0][0]
    t.transform.translation.y = msg[0][1]
    t.transform.translation.z = msg[0][2]
    # q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = msg[1][0]
    t.transform.rotation.y = msg[1][1]
    t.transform.rotation.z = msg[1][2]
    t.transform.rotation.w = msg[1][3]
    return t