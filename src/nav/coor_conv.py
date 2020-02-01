import math


def odom_to_map(x_o, y_o, xZ, yZ, r):
    if r == "s1":
        x = y_o+xZ
        y = -x_o+yZ
        return x, y
    else:
        x = -y_o+xZ
        y = x_o+yZ
        return x, y
def map_to_odom(x_m, y_m, xZ, yZ, r):
    if r == "s1":
        
        y = x_m-xZ
        x = -(y_m-yZ)
        return x, y
    else:
        y = -(x_m - xZ)
        x = (y_m-yZ)
        return x, y

# print(map_to_odom(7.22, 3.5, 7.7, 2.7, "s2"))
# print(odom_to_map(1, 0, 0.28, 4.4, "s1"))