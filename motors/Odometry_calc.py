import math
import numpy 

class OdometryCalc:
    def __init__(self, w=0.01):
        self.w = w
        self.o = 0
        self.Dl = 0
        self.Dr = 0
        self.d = 0

    def calc(self, dl=0, dr=0):
        self.Dr = dr
        self.Dl = dl
        self.o = self.o + (self.Dr + self.Dl)/self.w
        self.d = (self.Dr + self.Dl) / 2
        self.x = self.x + self.d*math.cos(self.o)
        self.y = self.y + self.d*math.sin(self.o)
        return self.x, self.y, self.o