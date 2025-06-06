import cv2
from picamera2 import Picamera2
import time
from pyapriltags import Detector
import numpy as np

picam2 = Picamera2()

WIDTH = 1536
HEIGH = 864
picam2.configure(picam2.create_preview_configuration({'size':(WIDTH,HEIGH)}))
picam2.start() 
nom = "antoine.png" # nom de l'image
picam2.capture_file(nom)