from picamera2 import Picamera2
import time

# Initialiser la caméra
picam2 = Picamera2()
modele = picam2.global_camera_info()[0]['Model']
picam2.stop()
picam2.stop()

modeles = camera_models = {
    "imx219": "Pi Camera V2",
    "imx708": "Pi Camera V3",
    "imx708_wide": "Pi Camera V3 Wide"}
print(modeles[modele])