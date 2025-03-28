import cv2
from picamera2 import Picamera2
import time
from pyapriltags import Detector
import numpy as np

picam2 = Picamera2()
WIDTH,HEIGH=3280,2464
picam2.configure(picam2.create_preview_configuration({'size':(WIDTH,HEIGH)}))
picam2.start()

at_detector = Detector(families="tag36h11",nthreads=1,quad_sigma=0.0,refine_edges=1,\
decode_sharpening=0.25,debug=0)

#coefficients de distorsion de la camera

mtx = np.array([[ 977.08159964 	,  0.00000000e+00,  789.18761132],[ 0.00000000e+00,  977.14004212, 434.47165678],[ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
dist = np.array([[-0.02727091,  0.1312434,   0.00479796,  0.00269239, -1.30723302]])

fx = mtx[0][0]
cx = mtx[0][2]
fy = mtx[1][1]
cy = mtx[1][2]


#Positions des tags dans l'environnement
listePoints3D = {6:(0,0,0)}

def capture():
    img=cv2.cvtColor(picam2.capture_array(),cv2.COLOR_BGR2GRAY) #prise d'une photo puis correction
    img_undistorded = cv2.undistort(img, mtx, dist, None, newCameraMatrix=mtx)
    #indication de la taille des tags, lancement de la detection
    tags=at_detector.detect(img_undistorded,estimate_tag_pose=True,camera_params=[fx,fy,cx,cy],tag_size=0.173) 
    return tags

def calculAngles(R):
    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0
    return np.degrees(np.array([x, y, z]))


matrice=np.array([[-1,0,0],[0,1,0],[0,0,1]])
while True:
    tags=capture()
    positions=[]
    positionMoyenne=np.array([0,0,0],dtype='float64')
    angles=[]
    angleMoyen=np.array([0,0,0],dtype='float64')
    for tag in tags:
        #calcul des angles suivant Xw, Yw et Zw
        angles.append(np.array(calculAngles(tag.pose_R)))
        
        pose=np.dot(np.transpose(tag.pose_R),tag.pose_t)
        #formule pour trouver la position  partir du resultat apriltag
        try :
           positions.append(np.dot(matrice,np.transpose(pose)[0])+np.array(listePoints3D[tag.tag_id])) 
        except : 
           print("tag inconnu detecte : ",tag.tag_id)
         
    #Calcul de la moyenne des différentes positions mesurées
    for position in positions:
        positionMoyenne+=position
    for angle in angles:
        angleMoyen+=angle
    n=len(positions)
    
    if n!=0:
        positionMoyenne=positionMoyenne/n
        print("position et nb tags : ", positionMoyenne,n)
        angleMoyen=angleMoyen/n
        print("angle : ", angleMoyen)
    
