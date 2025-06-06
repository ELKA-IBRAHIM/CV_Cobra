import math
from centrale_inirtielle import mesure_angles
from tf_luna import mesure_distance
import time


while 1:

    tangage, roulis, lacet = mesure_angles()
    d = mesure_distance()
    h = d*math.cos(tangage*math.pi/180)*math.cos(roulis*math.pi/180)
    print(h, "tangage",tangage,"roulis", roulis)
    time.sleep(1)