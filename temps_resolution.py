import cv2
from picamera2 import Picamera2
import time
from pyapriltags import Detector
import numpy as np
import os

modeles = camera_models = {
    "imx219": "V2 ",
    "imx708": "V3 ",
    "imx708_wide": "V3W"}

def temps_f_resolution(HEIGH = 3280, WIDTH = 2464, N = 10 ):
    """
    Renvoie le temps d'acquisition et de traitement en fonction de la résolotion choisie 
    et le nombre mesures pour moyenner cette durée
    """
        
    picam2 = Picamera2()


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
    listePoints3D = {0:(0,0,0),11:(0.70,0,0),12:(0,-0.90,0),13:(0.70,-0.90,0), 5:(0.70,-0.93,0), 17 : ((0.70,-0.33,0))}

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

    temps = 0
    for i in range(N):

        ti=time.time()
        matrice=np.array([[-1,0,0],[0,1,0],[0,0,1]])
    
            
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
            
        tf=time.time()
        temps += tf-ti
    
    picam2.stop()
    picam2.close()
    
    return(str(temps/N)+' s , '+ 'résolution: '+str(HEIGH)+'x'+str(WIDTH))


Resolutions = [(2592, 1944), (1920, 1080), (3280, 2464), (1640, 1232), (1640,922), (1280,720), (640,480)]



picam2 = Picamera2()
modele = modeles[picam2.global_camera_info()[0]['Model']]
picam2.stop()
picam2.close()

nom = f"{modele}_temps_resolution"
with open(nom, "w") as fichier:
    fichier.write("camera: "+modele+"\n")
    fichier.write("Résultats de la mesure de temps d'acquition et de traitement en fonction de la résolution.\n")
    fichier.write("le temps est moyenné sur 100 mesures \n \n")

    for resolution in Resolutions:
        fichier.write(temps_f_resolution(resolution[0], resolution[1])+"\n")
picam2.stop()
picam2.close()


      