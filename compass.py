
from UDPComms import Publisher

from time import sleep, time
import math

from HMC6343 import HMC6343

offset = 10

import board
import busio
import adafruit_lsm9ds1

class ComplementaryFilter:
    def __init__(self, K):
        self.K = K
        self.lastSin = math.sin(0)
        self.lastCos = math.cos(0)
        self.lastGyroTime = None
        self.lastGyro = 0
        

    def update_mag(self,heading):
        # heading is in degrees
        rad = math.radians(heading)
        self.lastSin = self.K * self.lastSin + (1-self.K) * math.sin(rad)
        self.lastCos = self.K * self.lastCos + (1-self.K) * math.cos(rad)

    def update_gyro(self,omega):
        # omega is in deg/s
        if self.lastGyroTime == None:
            self.lastGyroTime = time()
            return

        omega_rad = math.radians(omega)
        delta_t = time() - self.lastGyroTime
        self.lastGyroTime = time()

        rad = math.atan2(self.lastSin, self.lastCos) + omega_rad * delta_t
        self.lastSin = math.sin(rad)
        self.lastCos = math.cos(rad)

        self.lastGyro = (self.lastGyro + omega * delta_t) % 360

    def get_angle(self):
        rad = math.atan2(self.lastSin, self.lastCos)
        return math.degrees(rad) % 360

pub = Publisher(8220)
 
# I2C connection to IMU
i2c = busio.I2C(board.SCL, board.SDA)
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# I2C connection to IMU
compass = HMC6343()

# initialize filter
# TODO find good value
filt = ComplementaryFilter(0.99)

lastGyro = 0
lastMag = 0
lastPub = 0

while True:
    if time() - lastMag > 0.10:
        heading = compass.readHeading()
        filt.update_mag(heading)
        lastMag = time()

    if time() - lastGyro > 0.01:
        gyro_x, gyro_y, gyro_z = imu.gyro
        filt.update_gyro(-gyro_z)
        lastGyro = time()

    if time() - lastPub > 0.05:
        angle = filt.get_angle() + offset
        print(angle, heading, filt.lastGyro)
        pub.send({'angle':[angle, None, None],'mag':heading+offset})
        lastPub = time()

