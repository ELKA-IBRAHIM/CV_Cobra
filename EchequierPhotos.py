from picamera2 import Picamera2
import modele_cam
import os 
import cv2
import numpy as np
import time 

Resolutions = {'1': (640,480), '2': (1280,720) , '3':(2592, 1944), '4' : (1920, 1080), '5': (4608,2592)}

text_resolution = f"Choisir une résolution parmi les suivantes:\
    \n 1 : {Resolutions['1']} \
    \n 2 : {Resolutions['2']} \
    \n 3 : {Resolutions['3']} \
    \n 4 : {Resolutions['4']} \
    \n 5 : {Resolutions['5']} \
    \n Votre choix : "
choix_resolution = input(text_resolution)
assert choix_resolution in ['1','2','3','4'], "Choix impossible, choisir 1, 2, 3 ou 4"
WIDTH, HEIGH = Resolutions[choix_resolution]

# Demande du nombre de caméras utilisées.
n_cam = int(input("nombre de caméras 1 ou 2 : "))
#  Demande du nombre d'images désirées.
n = int(input("Nombre d'images désirées: "))

if n_cam == 1:
        

    modele0 = modele_cam.modele(0)

    chemin0 = os.getcwd()+f"/0_{modele0}_{str(WIDTH)}x{str(HEIGH)}Echequier"
    if not os.path.exists(chemin0): #Si le répertoire n'existe pas.
        os.mkdir(chemin0)
        
    

    
    cam0 = Picamera2(camera_num=0)
    
    cam0.configure(cam0.create_preview_configuration({'size':(WIDTH,HEIGH)}))

    time.sleep(1)  
    cam0.start()
    time.sleep(1)

    nb_im = 1
    while nb_im <= n:
        
        nom0 = chemin0 + f"/{modele0}_cam0Echequier{nb_im}.png"  # nom de l'image
        cam0.capture_file(nom0) # Enregistrer l'image

        print(f"Images enregistrées: {nb_im}/{n}") # exemple: Images enregistrées 1/10
        
        nb_im += 1
        time.sleep(2)
        print("be ready")
        time.sleep(2)
         #durée(en secondes) entre deux captures
    cam0.stop()
    cam0.close()
elif n_cam == 2:
    modele0 = modele_cam.modele(0)
    print("here")
    modele1 =  modele_cam.modele(1)
    # Chemin ou les photos d'échequier seront enregistrés
    chemin0 = os.getcwd()+f"/0_{modele0}_{str(WIDTH)}x{str(HEIGH)}Echequier"
    chemin1 = os.getcwd()+f"/1_{modele1}_{str(WIDTH)}x{str(HEIGH)}Echequier"




    if not os.path.exists(chemin0): #Si le répertoire n'existe pas
        os.mkdir(chemin0)

    if not os.path.exists(chemin1): #Si le répertoire n'existe pas
        os.mkdir(chemin1)


    ## Prise des photos de l'échequier

    n = int(input("Nombre d'images désirées: "))

    if n < 10: # Le nombre d'acquisitions doit être au moins égale à 10
        raise ValueError("Calibration impossible avec 0 images")
    else:
        cam0 = Picamera2(camera_num=0)
        cam0.configure(cam0.create_preview_configuration({'size':(WIDTH,HEIGH)}))
        time.sleep(1)
        cam0.start()
        time.sleep(1)
        cam1 = Picamera2(camera_num=1)
        cam1.configure(cam1.create_preview_configuration({'size':(WIDTH,HEIGH)}))
        time.sleep(1)  
        cam1.start()
        time.sleep(1)

        nb_im = 1
        while nb_im <= n:

            # Titre de l'image prise par la caméra branchée sur le port 0
            nom0 = chemin0 + f"/{modele0}_cam0Echequier{nb_im}.png" # nom de l'image
            cam0.capture_file(nom0) # Capture de l'image
            
            # Titre de l'image prise par la caméra branchée sur le port 0
            nom1 = chemin1 + f"/{modele1}_cam1Echequier{nb_im}.png" # nom de l'image
            cam1.capture_file(nom1) # Capture de l'image




            print(f"Images enregistrées: {str(nb_im)}/{str(n)}") # exemple: Images enregistrées 1/10
            
            nb_im += 1
            time.sleep(2) #durée(en secondes) entre deux captures
else :
    raise ValueError("Nombre de caméras 1 ou 2")