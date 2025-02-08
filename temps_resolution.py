import cv2
from picamera2 import Picamera2
import time
from pyapriltags import Detector
import numpy as np
import os
import modele_cam

"""
- Le programme reconnait la caméra utilisée, ainsi que la date de l'expérience.
- On renseigne la résolution 
- On renseigne N: le nombre de mesures; on ne peut pas se baser sur le temps de calcul pour une seule expérience
  donc on prend la durée moyenne de N expériences.
  EXEMPLE DU FICHIER SAUVEGARDÉ:
    --------Date de la mesure: 2025-02-06---------
    camera: V2
    Résultats de la mesure de temps d'acquition et de traitement en fonction de la résolution.
    le temps est moyenné sur 100 mesures  
    0.012184906005859374 s , résolution: 640x480
    0.04497494697570801 s , résolution: 1280x720
    0.25495595932006837 s , résolution: 2592x1944
    0.12182350158691406 s , résolution: 1920x1080
    0.67628493309021 s , résolution: 4608x2592
"""

def temps_f_resolution(HEIGH = 3280, WIDTH = 2464, N = 10 ):
    """
    HEIGH, WIDTH : la resolution choisie, 3280*2464 par défaut
    N : Le nombre d'expérience (La durrée prise sera la moyenne sur les N espériences)
    """
        
    picam2 = Picamera2()


    picam2.configure(picam2.create_preview_configuration({'size':(WIDTH,HEIGH)}))
    time.sleep(2)
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
    listePoints3D = {0:(0,0,0),1:(0.70,0,0),2:(0,-0.90,0),3:(0.70,-0.90,0), 4:(0.70,-0.93,0),5:(0.70,-1,0), 6 : ((0.70,-0.33,0))}

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
        print(n)
        
        if n!=0:
            positionMoyenne=positionMoyenne/n
            angleMoyen=angleMoyen/n
            
        tf=time.time()
        temps += tf-ti
    
    picam2.stop()
    picam2.close()
    
    return(f"{temps/N} s ,résolution: {HEIGH}x{WIDTH}  tags reconnus:{n} |temps moyyené sur {N} mesures")


Resolutions = [(640,480), (1280,720) , (2592, 1944), (1920, 1080), (4608,2592)]


modele = modele_cam.modele() #nom de la caméra utilisée.


current_time = time.localtime()
date_actuelle = time.strftime("%Y-%m-%d", current_time)

nom = f"/home/CobraVision2/Localisation/CV_Cobra/{modele}_temps_resolution.txt"

N = int(input("Choix de nombre d'éxpériences pour moyenner la durée: "))
with open(nom, "a") as fichier:
    fichier.write(f"--------Date de la mesure: {date_actuelle}---------\n")
    fichier.write(f"camera: {modele}\n")
    fichier.write("Résultats de la mesure de temps d'acquition et de traitement en fonction de la résolution.\n")

    for resolution in Resolutions:
        print(f"*-*-*mesure pour la résolution: {resolution[0]}x{resolution[1]}*-*-*")
        fichier.write(temps_f_resolution(resolution[0], resolution[1], N)+"\n")



      