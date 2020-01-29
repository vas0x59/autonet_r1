import rospy
import tf
import tf2_ros
import math

from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int16, Bool
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
import tf.transformations as t

def get_dist(x1, y1, x2, y2):
    return ((x1-x2) ** 2 + (y1-y2) ** 2)**0.5

def offset_yaw(yaw, zer_yaw):
    itog = yaw
    itog = yaw - zero_yaw
    if (itog > 1.0 * math.pi):
            itog -= 2.0 * math.pi
    if (itog < -1.0 * math.pi):
        itog+= 1.0 * math.pi
    return itog

def transform_xy_yaw(x, y, yaw, framefrom, frameto, tf_buffer):
    p = PoseStamped()
    p.header.frame_id = framefrom
    p.pose.position.x = x
    p.pose.position.y = y
    p.pose.orientation = orientation_from_euler(0, 0, yaw)
    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    pose_local = tf_buffer.transform(framefrom, frameto, TRANSFORM_TIMEOUT)
    target_x = pose_local.pose.position.x
    target_y = pose_local.pose.position.y
    target_yaw = euler_from_orientation(pose_local.orientation)[2]
    return target_x, target_y, target_yaw

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
