from picamera2 import Picamera2
import modele_cam
import os 
import cv2
import numpy as np
import time

modele  = modele_cam.modele()
time.sleep(2)

chemin = os.getcwd()+f"/{modele}_photos_resolutions" 

if not os.path.exists(chemin): #Si le répertoire n'existe pas
    os.mkdir(chemin)



Resolutions = [(640,480), (1280,720) , (2592, 1944), (1920, 1080), (4608,2592)]

for resolution in Resolutions:
    WIDTH,HEIGH = resolution
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration({'size':(WIDTH,HEIGH)}))
    picam2.start()
    nom = f"{chemin}/{modele}_{WIDTH}x{HEIGH}.png" # nom de l'image
    picam2.capture_file(nom)
    time.sleep(1) #durée(en secondes) entre deux captures
    picam2.stop()
    picam2.close()