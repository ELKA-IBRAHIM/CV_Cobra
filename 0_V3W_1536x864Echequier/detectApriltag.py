from pyapriltags import Detector
import cv2
import numpy as np
from picamera2 import Picamera2
import os
#Configuration de l'acquisition et paramètres de la calibration
picam2 = Picamera2()
WIDTH,HEIGH=1536,864
picam2.configure(picam2.create_preview_configuration({'size':(WIDTH,HEIGH)}))
picam2.start()
"""
fx=2530.69519
fy=2522.04812
cx=1758.66732
cy=1218.35539
"""
mtx = np.array([[ 977.08159964 	,  0.00000000e+00,  789.18761132],[ 0.00000000e+00,  977.14004212, 434.47165678],[ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
dist = np.array([[-0.02727091,  0.1312434,   0.00479796,  0.00269239, -1.30723302]])




fx = mtx[0][0]
print(fx)
cx = mtx[0][2]
print(cx)
fy = mtx[1][1]
print(fy)
cy = mtx[1][2]
print(cy)
#mtx = numpy.array([[fx,0,cx],[0,fy,cy],[0,0,1]])
#dist = numpy.array([[0.13432391,-0.13190146,0.00487085,0.01105209,-0.30871937]])
#Acquisition de l'image, correction et détection des tags présents sur l'image
img=cv2.cvtColor(picam2.capture_array(),cv2.COLOR_BGR2GRAY) #prise d'une photo
at_detector = Detector()
img_undistorded = cv2.undistort(img, mtx, dist, None, newCameraMatrix=mtx)
tags=at_detector.detect(img_undistorded, estimate_tag_pose=True,
camera_params=[fx,fy,cx,cy], tag_size=0.173)
print(tags)
#Affichage de l’image et pour chaque tags, des lignes reliant les coins et du

color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
for tag in tags:
    for idx in range(len(tag.corners)):
        cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)),tuple(tag.corners[idx, :].astype(int)),(0, 255,0),5)
    cv2.putText(color_img, str(tag.tag_id), org=(tag.corners[0,0].astype(int)+10,tag.corners[0, 1].astype(int)+10),fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0,255),thickness=5)
cv2.imshow('Detected tags', color_img)
k = cv2.waitKey(0)
if k == 27: # wait for ESC key to exit
    cv2.destroyAllWindows()
