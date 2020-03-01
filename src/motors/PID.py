import time


class PID:
    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.prev_time = time.time()
        self.dt = 0
        self.prev_error = 0
        self.first = True

    def calc(self, err):
        self.integral += err * d_time
        self.dt = (time.time() - self.prev_time)
        if self.first == False:
            self.res = self.kP*err + self.kD * \
                ((err-self.prev_error) / self.dt) + self.kI*self.integral
        else:
            self.res = self.kP*err
            self.first = False
        self.prev_error = err
        self.prev_time = time.time()
        return self.res
