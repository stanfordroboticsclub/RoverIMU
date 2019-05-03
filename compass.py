
from UDPComms import Publisher

from time import sleep
from HMC6343 import HMC6343

compass = HMC6343()
pub = Publisher(8220)

while True:
    heading = compass.readHeading()
    print(heading)
    pub.send({'angle':[heading, None, None]})
    sleep(0.10)
