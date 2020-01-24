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
        # self.prev_t = time.time()
        self.x = 0
        self.y = 0

        self.px = 0
        self.py = 0
        self.po = 0

        self.vx = 0
        self.vy = 0
        self.vo = 0

    def calc(self, dt, dl, dr):
        self.Dr = dr/dt
        self.Dl = dl/dt
        # self.prev_t = time.time()
        self.o = self.o + (self.Dr + self.Dl)/self.w
        self.d = (self.Dr + self.Dl) / 2
        self.x = self.x + self.d*math.cos(self.o)
        self.y = self.y + self.d*math.sin(self.o)

        self.px = self.x
        self.py = self.y
        self.po = self.o

        self.vx = (self.x-self.px)/dt
        self.vy = (self.y-self.py)/dt
        self.vo = (self.o-self.po)/dt
        return self.x, self.y, self.o, self.vx, self.vy, self.vo
    def set(self, x, y, o):
        self.x = x
        self.y = y
        self.o = o
