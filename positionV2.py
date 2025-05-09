import cv2
from picamera2 import Picamera2
import time
from pyapriltags import Detector
import numpy as np

cam1 = Picamera2(0)
WIDTH,HEIGH = 1536,864
cam1.configure(cam1.create_preview_configuration({'size':(WIDTH,HEIGH)}))
cam1.start()
cam2 = Picamera2(1)
WIDTH,HEIGH = 3280,2464
cam2.configure(cam2.create_preview_configuration({'size':(WIDTH,HEIGH)}))
cam2.start()

at_detector = Detector(families="tag36h11",nthreads=1,quad_sigma=0.0,refine_edges=1,\
decode_sharpening=0.25,debug=0)

#coefficients de distorsion de la camera

mtx = np.array([[ 977.08159964 	,  0.00000000e+00,  789.18761132],[ 0.00000000e+00,  977.14004212, 434.47165678],[ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
dist = np.array([[-0.02727091,  0.1312434,   0.00479796,  0.00269239, -1.30723302]])

fx = mtx[0][0]
cx = mtx[0][2]
fy = mtx[1][1]
cy = mtx[1][2]


#Positions des tags dans l'environnement en mètres
listePoints3D = {7:(0,0,0), 3:(0.2, 0.1375, 0), 6:(0.2, -0.1375, 0), 1:(0.2, 0.13, 0), 5:(0.2, -0.13, 0)}

def capture():
    img1=cv2.cvtColor(cam1.capture_array(),cv2.COLOR_BGR2GRAY) #prise d'une photo puis correction
    img_undistorded1 = cv2.undistort(img1, mtx, dist, None, newCameraMatrix=mtx)
    #indication de la taille des tags, lancement de la detection
    tags1=at_detector.detect(img_undistorded1,estimate_tag_pose=True,camera_params=[fx,fy,cx,cy],tag_size=0.173) 
    
    img2=cv2.cvtColor(cam2.capture_array(),cv2.COLOR_BGR2GRAY) #prise d'une photo puis correction
    img_undistorded2 = cv2.undistort(img2, mtx, dist, None, newCameraMatrix=mtx)
    #indication de la taille des tags, lancement de la detection
    tags2=at_detector.detect(img_undistorded2,estimate_tag_pose=True,camera_params=[fx,fy,cx,cy],tag_size=0.173) 
    

    return (tags1,tags2)

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
    tags1 = capture()[0]
    tags2 = capture()[1]

    positions1, positions2 = [],[]

    positionMoyenne1, positionMoyenne2 = np.array([0,0,0],dtype='float64'), np.array([0,0,0],dtype='float64')
    angles1, angles2 = [],[]

    angleMoyen1, angleMoyen2 = np.array([0,0,0],dtype='float64'),  np.array([0,0,0],dtype='float64')
    for tag1, tag2 in tags1, tags2:
        #calcul des angles suivant Xw, Yw et Zw
        angles1.append(np.array(calculAngles(tag1.pose_R)))
        angles2.append(np.array(calculAngles(tag2.pose_R)))
        
        pose1 = np.dot(np.transpose(tag1.pose_R),tag1.pose_t)
        pose2 = np.dot(np.transpose(tag2.pose_R),tag2.pose_t)
        
        #formule pour trouver la position  partir du resultat apriltag
        try :
           positions1.append(np.dot(matrice,np.transpose(pose1)[0])+np.array(listePoints3D[tag1.tag_id])) 
           positions2.append(np.dot(matrice,np.transpose(pose2)[0])+np.array(listePoints3D[tag2.tag_id])) 

        except : 
           print("tag inconnu detecte : ",tag1.tag_id)
         
    #Calcul de la moyenne des différentes positions mesurées
    for position1, position2 in positions1, positions2:
        positionMoyenne1 += position1
        positionMoyenne2 += position2

    for angle1, angle2 in angles1, angles2:
        angleMoyen1 += angle1
        angleMoyen2 += angle2
    n1, n2 = len(positions1), len(position2)
    
    if n1!=0 and n2 !=0 :
        positionMoyenne1 = positionMoyenne1/n1
        print("pos_cam1 : ", positionMoyenne1, "pos_cam2 : ", positionMoyenne1)
        angleMoyen1= angleMoyen1/n1
        angleMoyen2 = angleMoyen2/n2 
        print("angle1 : ", angleMoyen1, "angle2 : ", angleMoyen2)
    else:
        pass
    
