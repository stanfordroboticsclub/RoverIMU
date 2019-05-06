
from UDPComms import Publisher

from time import sleep
from HMC6343 import HMC6343
import math

class LowPass:
    def __init__(self, K):
        self.K = K
        self.lastSin = math.sin(0)
        self.lastCos = math.cos(0)
    def update(self,heading):
        rad = math.radians(heading)
        self.lastSin = self.K * self.lastSin + (1-self.K) * math.sin(rad)
        self.lastCos = self.K * self.lastCos + (1-self.K) * math.cos(rad)

    def get_angle(self):
        rad = math.atan2(self.lastSin, self.lastCos)
        return math.degrees(rad) % 360

compass = HMC6343()
pub = Publisher(8220)
filt = LowPass(0.9)

while True:
    heading = compass.readHeading()
    filt.update(heading)
    angle = filt.get_angle()
    print(heading, angle)
    pub.send({'angle':[angle, None, None]})
    sleep(0.10)
