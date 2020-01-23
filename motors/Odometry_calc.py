import math
import numpy
import time


class OdometryCalc:
    def __init__(self, w=0.01):
        self.w = w
        self.o = 0
        self.Dl = 0
        self.Dr = 0
        self.d = 0
        self.prev_t = time.time()

    def calc(self, dl=0, dr=0):
        self.Dr = dr/(time.time() - self.prev_t)
        self.Dl = dl/(time.time() - self.prev_t)
        self.prev_t = time.time()
        self.o = self.o + (self.Dr + self.Dl)/self.w
        self.d = (self.Dr + self.Dl) / 2
        self.x = self.x + self.d*math.cos(self.o)
        self.y = self.y + self.d*math.sin(self.o)
        return self.x, self.y, self.o
