import os 
import cv2
import numpy as np

# Chemin ou les photos d'échequier seront enregistrés
chemin0 = "/home/CobraVision2/Localisation/0PhotosEchequier" 
chemin1 = "/home/CobraVision2/Localisation/1PhotosEchequier" 



if not os.path.exists(chemin0): #Si le répertoire n'existe pas
    os.mkdir(chemin0)

if not os.path.exists(chemin1): #Si le répertoire n'existe pas
    os.mkdir(chemin1)


## Prise des photos de l'échequier

n = int(input("Nombre d'images désirée"))

if n < 10: # Le nombre d'acquisitions doit être au moins égale à 10
    raise ValueError("Calibration impossible avec 0 images")
else:
    cap0 = cv2.VideoCapture(0)
    if not cap0.isOpened():
        print("Impossible d'ouvrir la caméra 0")
    
    cap1 = cv2.VideoCapture(1)
    if not cap1.isOpened():
        print("Impossible d'ouvrir la caméra 1")
    
    
    nb_im = 1
    while nb_im <= n:

        ret0 , frame0 = cap0.read() #Prise de l'image
        if not ret0:
            print("Erreur lors de la capture de l'image[cam0]")

        nom0 = chemin0 + '/ Eam0Echequier'+str(nb_im)+'.png' # nom de l'image
        cv2.imwrite(nom0, frame0) # Enregistrer l'image

        ret1 , frame1 = cap1.read() #Prise de l'image
        if not ret1:
            print("Erreur lors de la capture de l'image[cam1]")
        nom1 = chemin1 + '/Cam1Echequier'+str(nb_im)+'.png' # nom de l'image
        cv2.imwrite(nom1, frame1) # Enregistrer l'image




        print('Images enregistrées',str(nb_im),'/',str(n)) # exemple: Images enregistrées 1/10
        
        nb_im += 1