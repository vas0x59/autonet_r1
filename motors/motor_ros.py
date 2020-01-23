import rospy
import tf


from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

from Motor import Motor
from Odometry_calc import OdometryCalc
import json
from PID import PID
config = json.load(open("config.json"))

robot_W = config["robot_W"]
wheel_d = config["wheel_d"]
update_rate = config["update_rate"]
frame_name = config["frame_name"]
kp = config["motor_v_pid"]["p"]
ki = config["motor_v_pid"]["i"]
kd = config["motor_v_pid"]["d"]

m1 = Motor(n=1, d=wheel_d)
m2 = Motor(n=2, d=wheel_d)
m1_pid = PID(kp, ki, kd)
m2_pid = PID(kp, ki, kd)

odom_pub = rospy.Publisher('odom', Odometry, queue_size=50)
odom_broadcaster = tf.TransformBroadcaster()

encoder1 = rospy.Publisher('/encoder1', Float32, queue_size=10)
encoder2 = rospy.Publisher('/encoder2', Float32, queue_size=10)

encoder1_v = rospy.Publisher('/encoder1_v', Float32, queue_size=10)
encoder2_v = rospy.Publisher('/encoder2_v', Float32, queue_size=10)


odometry_c = OdometryCalc(w=robot_W)

m1_target_v = 0
m2_target_v = 0

# m1_v = 0
# m2_v = 0


def m1tv_clb(data):
    global m1_target_v
    m1_target_v = data.data


def m2tv_clb(data):
    global m2_target_v
    m2_target_v = data.data


rospy.Subscriber("/motor1", Float32, m1tv_clb)
rospy.Subscriber("/motor2", Float32, m1tv_clb)

rospy.init_node('motor_ros', anonymous=True)


def control_motors():
    global m1_target_v, m2_target_v, m1, m2, m1_pid, m2_pid
    m1.set_power(m1_pid.calc(m1_target_v - m1.get_v_ms()))
    m2.set_power(m2_pid.calc(m2_target_v - m2.get_v_ms()))


last_time = rospy.Time.now()


def calc_odometry():
    global encoder1, encoder2, odom_broadcaster, m1, m2, odom_pub, last_time, encoder1_v, encoder2_v

    encoder1.publish(m1.get_m())
    encoder2.publish(m2.get_m())
    encoder1_v.publish(m1.get_v_ms())
    encoder2_v.publish(m2.get_v_ms())

    current_time = rospy.Time.now()
    x, y, th, vx, vy, vth = odometry_c.calc(current_time - last_time,
                                            m1.get_m(), m2.get_m())
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
    odom_broadcaster.sendTransform(
        (x, y, 0.),
        odom_quat,
        current_time,
        "base_link",
        "odom"
    )

    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set the position
    odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

    # set the velocity
    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

    # publish the message
    odom_pub.publish(odom)
    last_time = current_time


def do():
    control_motors()
    calc_odometry()
    # pass


r = rospy.Rate(update_rate)  # 10hz
while not rospy.is_shutdown():
    do()
    r.sleep()

# rospy.
# odometry_c.calc()


# def calc_odometry():
#     # global robot_W
#     O(t+1)  = O(t) + (Dr - Dl)/W
