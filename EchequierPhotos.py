from picamera2 import Picamera2

import os 
import cv2
import numpy as np
import time 

n_cam = int(input("nombre de caméras 1 ou 2 : "))
if n_cam == 1:
    chemin0 = os.getcwd()+"/0PhotosEchequier" 
    if not os.path.exists(chemin0): #Si le répertoire n'existe pas
        os.mkdir(chemin0)
        
    
    n = int(input("Nombre d'images désirée"))

    if n < 10: # Le nombre d'acquisitions doit être au moins égale à 10
        raise ValueError("Calibration impossible avec 0 images")
    else:
        cam0 = Picamera2(0)
        cam0.configure(cam0.create_still_configuration())
        time.sleep(1)  
        cam0.start()
        time.sleep(1)

        nb_im = 1
        while nb_im <= n:

            nom0 = chemin0 + '/cam0Echequier'+str(nb_im)+'.png' # nom de l'image
            cam0.capture_file(nom0) # Enregistrer l'image

            print('Images enregistrées',str(nb_im),'/',str(n)) # exemple: Images enregistrées 1/10
            
            nb_im += 1
            time.sleep(2) #durée(en secondes) entre deux captures
elif n_cam == 2:
        
    # Chemin ou les photos d'échequier seront enregistrés
    chemin0 = os.getcwd()+"/0PhotosEchequier" 
    chemin1 = os.getcwd()+"/1PhotosEchequier" 



    if not os.path.exists(chemin0): #Si le répertoire n'existe pas
        os.mkdir(chemin0)

    if not os.path.exists(chemin1): #Si le répertoire n'existe pas
        os.mkdir(chemin1)


    ## Prise des photos de l'échequier

    n = int(input("Nombre d'images désirée"))

    if n < 10: # Le nombre d'acquisitions doit être au moins égale à 10
        raise ValueError("Calibration impossible avec 0 images")
    else:
        cam0 = Picamera2(0)
        cam0.configure(cam0.create_still_configuration())
        time.sleep(1)
        cam0.start()
        time.sleep(1)
        cam1 = Picamera2(1)
        cam1.configure(cam1.create_still_configuration())
        time.sleep(1)  
        cam1.start()
        time.sleep(1)

        nb_im = 1
        while nb_im <= n:

            
            nom0 = chemin0 + '/cam0Echequier'+str(nb_im)+'.png' # nom de l'image
            cam0.capture_file(nom0)
            
            
            nom1 = chemin1 + '/cam1Echequier'+str(nb_im)+'.png' # nom de l'image
            cam1.capture_file(nom1) # Enregistrer l'image




            print('Images enregistrées',str(nb_im),'/',str(n)) # exemple: Images enregistrées 1/10
            
            nb_im += 1
            time.sleep(2) #durée(en secondes) entre deux captures
else :
    raise ValueError("Nombre de caméras 1 ou 2")