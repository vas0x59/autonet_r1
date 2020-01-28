import rospy
import tf
import tf2_ros


from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int16, Bool
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
import tf.transformations as t

def get_transform(msg):
    # br = tf2_ros.TransformBroadcaster()
    ts = TransformStamped()

    ts.header.stamp = msg[2]
    ts.header.frame_id = msg[4]
    ts.child_frame_id = msg[3]
    ts.transform.translation.x = msg[0][0]
    ts.transform.translation.y = msg[0][1]
    ts.transform.translation.z = msg[0][2]
    # q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    ts.transform.rotation.x = msg[1][0]
    ts.transform.rotation.y = msg[1][1]
    ts.transform.rotation.z = msg[1][2]
    ts.transform.rotation.w = msg[1][3]
    return ts

# from geometry_msgs.msg import Quaternion, Vector3, Point
# import tf.transformations as t


def orientation_from_quaternion(q):
    return Quaternion(*q)


def orientation_from_euler(roll, pitch, yaw):
    q = t.quaternion_from_euler(roll, pitch, yaw)
    return orientation_from_quaternion(q)


def quaternion_from_orientation(o):
    return o.x, o.y, o.z, o.w


def euler_from_orientation(o):
    q = quaternion_from_orientation(o)
    return t.euler_from_quaternion(q)


def vector3_from_point(p):
    return Vector3(p.x, p.y, p.z)


def point_from_vector3(v):
    return Point(v.x, v.y, v.z)