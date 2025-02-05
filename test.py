from picamera2 import Picamera2
import time

# Initialiser la caméra
picam2 = Picamera2()
print(picam2.global_camera_info())
modele = picam2.global_camera_info()[0]['Model']
picam2.stop()
picam2.stop()

modeles = camera_models = {
    "imx219": "V2 ",
    "imx708": "V3 ",
    "imx708_wide": "V3W"}
print(modeles[modele])