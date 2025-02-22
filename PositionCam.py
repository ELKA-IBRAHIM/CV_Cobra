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

fx=2.54535633e+03
fy=2.54786131e+03
cx=1.56751977e+03
cy=1.27877378e+03

#coefficients de distorsion de la camera
dist=np.array([ 0.16388869,-0.21043407,0.00532856,-0.00619909,-0.15718788]) 
mtx=np.array([[fx,0,cx],[0,fy,cy],[0,0,1]]) #matrice de la camera

#Positions des tags dans l'environnement
listePoints3D = {2:(0.194,0,0),4:(0,0.235,0),15:(0.194,0.235,0), 0:(0,0,0) }

def Detection_Tags():
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


ti=time.time()
matrice=np.array([[-1,0,0],[0,1,0],[0,0,1]])
def localisation():
    """Renvoie:
    (x, y, z, alpha)
     - La position de la caméra (x, y, z) dans le repère du sol
     - L'angle de lacet (c'est le seul qui nous interesse dans le cas d'un dirigeable
     """
    
    tags=Detection_Tags()
    
    positions=[]
    angles=[]
    
    positionMoyenne=np.array([0,0,0],dtype='float64')
    angleMoyen=np.array([0,0,0],dtype='float64')
    
    for tag in tags:

        angles.append(np.array(calculAngles(tag.pose_R)))
        
        pose=np.dot(np.transpose(tag.pose_R),tag.pose_t)
       
        try :
           positions.append(np.dot(matrice,np.transpose(pose)[0])+np.array(listePoints3D[tag.tag_id])) 
        except : 
           print("Tag inconnu")
         
    for position in positions:
        positionMoyenne += position
    for angle in angles:
        angleMoyen += angle
    
    n=len(positions)
    
    if n!=0:
        positionMoyenne=positionMoyenne/n
        angleMoyen=angleMoyen/n

        #            X                    Y                     Z              Lacet
        return(positionMoyenne[0], positionMoyenne[1], positionMoyenne[2], angleMoyen[2])
        
    
    tf=time.time()
    print("temps",str(tf-ti),"secondes")
    ti=tf
while True:
    print(localisation())
