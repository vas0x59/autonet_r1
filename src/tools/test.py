import math
def offset_yaw(yaw, zero_yaw):
    itog = yaw
    itog = yaw - zero_yaw
    if (itog > 1.0 * math.pi):
            itog -= 2.0 * math.pi
    if (itog < -1.0 * math.pi):
        itog+= 2.0 * math.pi
    return itog


print(offset_yaw(float(input()), 0))



















