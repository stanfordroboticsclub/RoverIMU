
from UDPComms import Publisher

from time import sleep
from HMC6343 import HMC6343


compass = HMC6343()
while True:
    heading = compass.readHeading()
    print(heading)
    sleep(0.10)
